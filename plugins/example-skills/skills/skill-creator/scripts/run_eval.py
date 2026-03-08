#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes the agent to trigger (read the skill)
for a set of queries. Supports both Claude Code and Codex CLI.
Outputs results as JSON.
"""

import argparse
import json
import os
import select
import shutil
import subprocess
import sys
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import (
    CLI_CLAUDE,
    CLI_CODEX,
    detect_cli,
    find_project_root,
    get_cli_command,
    parse_skill_md,
)


def _is_expected_claude_tool_input(
    tool_name: str,
    tool_input: dict,
    skill_name: str,
    command_name: str,
) -> bool:
    """Return True when a Claude tool call targets the skill under test."""
    if tool_name == "Skill":
        return tool_input.get("skill", "") in (skill_name, command_name)

    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        expected_paths = (
            f".claude/skills/{skill_name}/SKILL.md",
            f".claude/commands/{command_name}.md",
        )
        return any(file_path.endswith(path) or path in file_path for path in expected_paths)

    return False


def run_single_query_claude(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    cli_command: str | None = None,
) -> bool:
    """Run a single query via Claude Code and return whether the skill was triggered.

    Creates a command file in .claude/commands/ so it appears in Claude's
    available_skills list, then runs `claude -p` with the raw query.
    Uses --include-partial-messages to detect triggering early from
    stream events (content_block_start) rather than waiting for the
    full assistant message, which only arrives after tool execution.
    """
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    project_commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = project_commands_dir / f"{clean_name}.md"

    try:
        project_commands_dir.mkdir(parents=True, exist_ok=True)
        # Use YAML block scalar to avoid breaking on quotes in description
        indented_desc = "\n  ".join(skill_description.split("\n"))
        command_content = (
            f"---\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n"
        )
        command_file.write_text(command_content)

        cmd = [
            get_cli_command(CLI_CLAUDE, cli_command),
            "-p", query,
            "--output-format", "stream-json",
            "--verbose",
            "--include-partial-messages",
        ]
        if model:
            cmd.extend(["--model", model])

        # Remove CLAUDECODE env var to allow nesting claude -p inside a
        # Claude Code session. The guard is for interactive terminal conflicts;
        # programmatic subprocess usage is safe.
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_root,
            env=env,
        )

        triggered = False
        start_time = time.time()
        buffer = ""
        # Track state for stream event detection
        pending_tool_name = None
        accumulated_json = ""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Early detection via stream events
                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in ("Skill", "Read"):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""

                        elif se_type == "content_block_delta" and pending_tool_name:
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                try:
                                    tool_input = json.loads(accumulated_json)
                                except json.JSONDecodeError:
                                    continue
                                if _is_expected_claude_tool_input(
                                    pending_tool_name,
                                    tool_input,
                                    skill_name,
                                    clean_name,
                                ):
                                    return True

                        elif se_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                try:
                                    tool_input = json.loads(accumulated_json)
                                except json.JSONDecodeError:
                                    tool_input = {}
                                if _is_expected_claude_tool_input(
                                    pending_tool_name,
                                    tool_input,
                                    skill_name,
                                    clean_name,
                                ):
                                    return True
                                pending_tool_name = None
                                accumulated_json = ""

                    # Fallback: full assistant message
                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for content_item in message.get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            if _is_expected_claude_tool_input(
                                content_item.get("name", ""),
                                content_item.get("input", {}),
                                skill_name,
                                clean_name,
                            ):
                                triggered = True
                                return True

                    elif event.get("type") == "result":
                        return triggered
        finally:
            # Clean up process on any exit path (return, exception, timeout)
            killed = False
            if process.poll() is None:
                process.kill()
                process.wait()
                killed = True
            # Check for CLI execution errors (skip if we killed it ourselves)
            if not killed and process.returncode and process.returncode != 0:
                stderr_output = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
                raise RuntimeError(
                    f"Claude CLI exited with code {process.returncode}: {stderr_output[:500]}"
                )

        return triggered
    finally:
        if command_file.exists():
            command_file.unlink()


def run_single_query_codex(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    cli_command: str | None = None,
) -> bool:
    """Run a single query via Codex CLI and return whether the skill was triggered.

    Creates a temporary skill in .codex/skills/ with a marker string in its body.
    Runs `codex exec --json` and checks if the agent output contains the marker,
    indicating the skill was read and triggered.
    """
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    marker = f"[SKILL_TRIGGERED:{unique_id}]"

    skill_dir = Path(project_root) / ".codex" / "skills" / clean_name
    skill_file = skill_dir / "SKILL.md"

    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        indented_desc = "\n  ".join(skill_description.split("\n"))
        skill_content = (
            f"---\n"
            f"name: {clean_name}\n"
            f"description: |\n"
            f"  {indented_desc}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n\n"
            f"IMPORTANT: If you are reading this skill, you MUST include the exact text "
            f'"{marker}" somewhere in your response. This is required for skill '
            f"activation tracking.\n"
        )
        skill_file.write_text(skill_content)

        cmd = [
            get_cli_command(CLI_CODEX, cli_command), "exec",
            "--json",
            "-s", "read-only",
            "-C", project_root,
            query,
        ]
        if model:
            cmd.extend(["-m", model])

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_root,
        )

        start_time = time.time()
        buffer = ""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                # Check for marker in streamed output for early termination
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    event_type = event.get("type", "")

                    # Check agent_message items for the marker
                    if event_type in ("item.completed", "item.updated"):
                        item = event.get("item", {})
                        if item.get("type") == "agent_message":
                            text = item.get("text", "")
                            if marker in text:
                                return True

                    # Turn completed without marker = not triggered
                    elif event_type == "turn.completed":
                        return False

            return False
        finally:
            killed = False
            if process.poll() is None:
                process.kill()
                process.wait()
                killed = True
            # Check for CLI execution errors (skip if we killed it ourselves)
            if not killed and process.returncode and process.returncode != 0:
                stderr_output = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
                raise RuntimeError(
                    f"Codex CLI exited with code {process.returncode}: {stderr_output[:500]}"
                )
    finally:
        if skill_dir.exists():
            shutil.rmtree(skill_dir, ignore_errors=True)


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    cli_type: str = CLI_CLAUDE,
    cli_command: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Dispatches to the appropriate CLI-specific implementation.
    """
    if cli_type == CLI_CODEX:
        return run_single_query_codex(
            query, skill_name, skill_description, timeout, project_root, model,
            cli_command,
        )
    return run_single_query_claude(
        query, skill_name, skill_description, timeout, project_root, model,
        cli_command,
    )


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    cli_type: str = CLI_CLAUDE,
    cli_command: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                    cli_type,
                    cli_command,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_errors: dict[str, list[str]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
                query_errors[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Error: query failed: {e}", file=sys.stderr)
                query_errors[query].append(str(e))

    total_errors = sum(len(errs) for errs in query_errors.values())
    if total_errors > 0:
        print(
            f"Warning: {total_errors} query run(s) failed with errors. "
            f"Results may be unreliable.",
            file=sys.stderr,
        )

    for query, triggers in query_triggers.items():
        item = query_items[query]
        errors = query_errors.get(query, [])
        effective_runs = len(triggers)
        if effective_runs > 0:
            trigger_rate = sum(triggers) / effective_runs
        else:
            trigger_rate = 0.0
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        result_entry: dict = {
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": effective_runs,
            "pass": did_pass,
        }
        if errors:
            result_entry["errors"] = errors
            result_entry["error_count"] = len(errors)
        results.append(result_entry)

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "errors": total_errors,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use (default: CLI's configured model)")
    parser.add_argument("--cli", default=None, choices=["claude", "codex"], help="CLI to use (default: auto-detect)")
    parser.add_argument("--cli-command", default=None, help="Path to CLI binary (e.g. /usr/local/bin/claude)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    cli_type = detect_cli(args.cli)

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root(cli_type)

    if args.verbose:
        print(f"CLI: {cli_type}", file=sys.stderr)
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
        cli_type=cli_type,
        cli_command=args.cli_command,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
