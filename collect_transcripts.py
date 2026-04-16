"""Collect and export AI coding assistant session transcripts.

Searches OS-dependent locations for session data from Copilot CLI and
Claude Code, presents an interactive menu of discovered sessions (with
timestamp and the first few lines of the first user prompt), and
exports the selected session(s) as a zip bundle containing:

    transcript.md       Readable Markdown summary
    raw/<tool>_<id>.*   Original JSONL (or .md) session files for grading

Usage
-----
    python collect_transcripts.py [--output ai_transcript.zip]

Sources searched
----------------
    Copilot CLI : ~/.copilot/session-state/<uuid>/events.jsonl
    Claude Code : ~/.claude/projects/<project>/<uuid>.jsonl
    Manual      : ./copilot-session-*.md, ./*.transcript.md
"""

import argparse
import io
import json
import os
import platform
import re
import zipfile
from datetime import datetime
from pathlib import Path


# ---------- OS-dependent paths ----------

def _home():
    if platform.system() == "Windows":
        return Path(os.environ.get("USERPROFILE", Path.home()))
    return Path.home()


def _copilot_cli_session_dir():
    return _home() / ".copilot" / "session-state"


def _claude_projects_dir():
    return _home() / ".claude" / "projects"


# ---------- Copilot CLI parser ----------

def _parse_copilot_cli_session(session_dir):
    """Parse a Copilot CLI session directory, return (start_time, first_prompt, cwd).

    Events file format: each line is a JSON object with at least
    {"type": ..., "data": {...}, "timestamp": "ISO 8601", ...}.

    The first user prompt is the first record with type == "user.message",
    from which we read data.content.
    """
    events_file = session_dir / "events.jsonl"
    if not events_file.is_file():
        return None

    start_time = None
    first_prompt = None
    cwd = None

    try:
        with open(events_file, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                rtype = record.get("type", "")
                data = record.get("data", {})
                ts = record.get("timestamp")

                if rtype == "session.start":
                    start_time = data.get("startTime") or ts
                    cwd = data.get("context", {}).get("cwd")

                if first_prompt is None and rtype == "user.message":
                    content = data.get("content", "")
                    if isinstance(content, str) and content.strip():
                        first_prompt = content.strip()
                        if start_time is None:
                            start_time = ts
                        break
    except OSError:
        return None

    if start_time is None:
        start_time = datetime.fromtimestamp(events_file.stat().st_mtime).isoformat() + "Z"

    return {
        "tool": "Copilot CLI",
        "path": events_file,
        "session_dir": session_dir,
        "timestamp": start_time,
        "first_prompt": first_prompt or "(no user message yet)",
        "cwd": cwd,
    }


# ---------- Claude Code parser ----------

_CLAUDE_META_PREFIXES = (
    "<local-command-caveat>",
    "<local-command-stdout>",
    "<command-name>",
    "<command-message>",
    "<command-args>",
    "<system-reminder>",
)


def _parse_claude_session(jsonl_file):
    """Parse a Claude Code session file, return timestamp and first real user prompt.

    Claude Code stores each session as a JSONL file where each line is a
    record with {"type": "user"|"assistant"|..., "message": {"role": ...,
    "content": ...}, "timestamp": "ISO 8601", "sessionId": ..., "cwd": ...}.

    We skip records with isMeta == True and messages whose content starts
    with CLI system tags like <command-name> or <system-reminder>.
    """
    if not jsonl_file.is_file():
        return None

    start_time = None
    first_prompt = None
    cwd = None

    try:
        with open(jsonl_file, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if start_time is None:
                    ts = record.get("timestamp")
                    if ts:
                        start_time = ts
                if cwd is None:
                    cwd = record.get("cwd")

                if first_prompt is not None:
                    continue

                if record.get("type") != "user" or record.get("isMeta"):
                    continue

                msg = record.get("message", {})
                if msg.get("role") != "user":
                    continue

                content = msg.get("content")
                if isinstance(content, list):
                    # Some user records have a list of content parts
                    parts = [p.get("text", "") for p in content if isinstance(p, dict)]
                    content = " ".join(p for p in parts if p)
                if not isinstance(content, str) or not content.strip():
                    continue
                if content.lstrip().startswith(_CLAUDE_META_PREFIXES):
                    continue

                first_prompt = content.strip()
    except OSError:
        return None

    if start_time is None:
        start_time = datetime.fromtimestamp(jsonl_file.stat().st_mtime).isoformat() + "Z"

    return {
        "tool": "Claude Code",
        "path": jsonl_file,
        "session_dir": jsonl_file.parent,
        "timestamp": start_time,
        "first_prompt": first_prompt or "(no user message found)",
        "cwd": cwd,
    }


# ---------- Manual transcript parser ----------

def _parse_manual_file(md_file, tool_label):
    ts = datetime.fromtimestamp(md_file.stat().st_mtime).isoformat() + "Z"
    try:
        text = md_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""
    first_prompt = text.strip().splitlines()[0] if text.strip() else "(empty file)"
    return {
        "tool": tool_label,
        "path": md_file,
        "session_dir": md_file.parent,
        "timestamp": ts,
        "first_prompt": first_prompt,
        "cwd": None,
    }


# ---------- Discovery ----------

def discover_sessions():
    sessions = []

    # Copilot CLI
    cli_root = _copilot_cli_session_dir()
    if cli_root.is_dir():
        for entry in cli_root.iterdir():
            if entry.is_dir():
                info = _parse_copilot_cli_session(entry)
                if info:
                    sessions.append(info)

    # Claude Code
    claude_root = _claude_projects_dir()
    if claude_root.is_dir():
        for project_dir in claude_root.iterdir():
            if not project_dir.is_dir():
                continue
            for jsonl_file in project_dir.glob("*.jsonl"):
                info = _parse_claude_session(jsonl_file)
                if info:
                    sessions.append(info)

    # Manual exports in the current directory
    for md in Path.cwd().glob("copilot-session-*.md"):
        sessions.append(_parse_manual_file(md, "Copilot CLI export"))
    for md in Path.cwd().glob("*.transcript.md"):
        sessions.append(_parse_manual_file(md, "Manual transcript"))

    # Sort newest first
    def _sort_key(s):
        return s["timestamp"] or ""
    sessions.sort(key=_sort_key, reverse=True)
    return sessions


# ---------- Display ----------

def _format_timestamp(iso):
    """Convert an ISO 8601 timestamp to a friendlier display form."""
    if not iso:
        return "(no time)"
    try:
        # Handle trailing Z and microseconds
        s = iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return iso[:19]


def _truncate(text, max_chars, max_lines=3):
    lines = [l for l in text.splitlines() if l.strip()]
    preview = "\n".join(lines[:max_lines])
    preview = re.sub(r"\s+", " ", preview).strip()
    if len(preview) > max_chars:
        preview = preview[: max_chars - 3].rstrip() + "..."
    return preview


def display_sessions(sessions):
    if not sessions:
        print("\nNo AI sessions found on this machine.")
        print("\nManual options:")
        print("  - Copilot CLI:  run /share file ai_transcript.md inside your session")
        print("  - VS Code Chat: right-click the chat session and choose Export")
        print("  - Fallback:     copy-paste your prompts/responses into ai_transcript.md")
        return

    print(f"\nFound {len(sessions)} AI session(s):\n")
    header = f"{'#':>3}  {'Tool':<20}  {'Started':<19}  {'CWD / First prompt'}"
    print(header)
    print("-" * len(header))
    for i, s in enumerate(sessions, 1):
        when = _format_timestamp(s["timestamp"])
        cwd = s.get("cwd") or ""
        cwd_label = f"[{Path(cwd).name}] " if cwd else ""
        preview = _truncate(s["first_prompt"], max_chars=80)
        print(f"{i:>3}  {s['tool']:<20}  {when:<19}  {cwd_label}{preview}")


# ---------- Selection and export ----------

def parse_selection(text, total):
    indices = set()
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            try:
                start, end = part.split("-", 1)
                for i in range(int(start), int(end) + 1):
                    if 1 <= i <= total:
                        indices.add(i - 1)
            except ValueError:
                pass
        else:
            try:
                i = int(part)
                if 1 <= i <= total:
                    indices.add(i - 1)
            except ValueError:
                pass
    return sorted(indices)


def _export_copilot_cli(events_file, out):
    with open(events_file, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            rtype = record.get("type", "")
            data = record.get("data", {})
            if rtype == "user.message":
                content = data.get("content", "")
                if isinstance(content, str) and content.strip():
                    out.write(f"**User:**\n\n{content.strip()}\n\n")
            elif rtype == "assistant.message":
                content = data.get("content", "")
                if isinstance(content, str) and content.strip():
                    out.write(f"**Assistant:**\n\n{content.strip()}\n\n")


def _export_claude(jsonl_file, out):
    with open(jsonl_file, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("isMeta"):
                continue
            msg = record.get("message", {})
            role = msg.get("role")
            content = msg.get("content")
            if isinstance(content, list):
                parts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
                content = "\n".join(p for p in parts if p)
            if not isinstance(content, str) or not content.strip():
                continue
            if content.lstrip().startswith(_CLAUDE_META_PREFIXES):
                continue
            label = "User" if role == "user" else "Assistant"
            out.write(f"**{label}:**\n\n{content.strip()}\n\n")


_TOOL_SLUG = {
    "Copilot CLI": "copilot_cli",
    "Claude Code": "claude_code",
    "Copilot CLI export": "copilot_cli_export",
    "Manual transcript": "manual",
}


def _raw_archive_name(session):
    """Build a stable filename for the original session file inside the zip."""
    slug = _TOOL_SLUG.get(session["tool"], "session")
    stem = session["path"].stem
    suffix = session["path"].suffix or ".jsonl"
    return f"raw/{slug}_{stem}{suffix}"


def export_sessions(sessions, indices, output_path):
    """Write a zip bundle containing transcript.md plus raw session files."""
    buf = io.StringIO()
    buf.write("# AI Interaction Transcript\n\n")
    buf.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    buf.write("See the `raw/` directory in this archive for the original\n")
    buf.write("session files (JSONL) with per-turn timestamps, tool calls,\n")
    buf.write("and other metadata that the Markdown summary below omits.\n\n")

    for idx in indices:
        s = sessions[idx]
        when = _format_timestamp(s["timestamp"])
        buf.write(f"---\n\n## {s['tool']} - {when}\n\n")
        buf.write(f"Source: `{s['path']}`\n\n")
        if s.get("cwd"):
            buf.write(f"Working directory: `{s['cwd']}`\n\n")
        buf.write(f"Raw file in this archive: `{_raw_archive_name(s)}`\n\n")
        try:
            if s["tool"] == "Copilot CLI":
                _export_copilot_cli(s["path"], buf)
            elif s["tool"] == "Claude Code":
                _export_claude(s["path"], buf)
            else:
                buf.write(s["path"].read_text(encoding="utf-8", errors="replace"))
                buf.write("\n")
        except OSError as e:
            buf.write(f"(Error reading session: {e})\n\n")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("transcript.md", buf.getvalue())
        for idx in indices:
            s = sessions[idx]
            try:
                zf.writestr(_raw_archive_name(s),
                            s["path"].read_bytes())
            except OSError as e:
                zf.writestr(
                    _raw_archive_name(s) + ".error",
                    f"Could not read original session: {e}\n".encode("utf-8"),
                )

    print(f"\nExported {len(indices)} session(s) to {output_path}")
    print("Archive contains: transcript.md (readable summary) + raw/ (original JSONL).")


# ---------- Main ----------

def _inside_git_working_tree(path):
    """Return the working-tree root containing path, or None."""
    p = Path(path).resolve()
    if not p.exists() or p.is_file():
        p = p.parent
    for candidate in [p, *p.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def _warn_if_in_git(output_path):
    """Print a loud warning and return False if output is inside a git working tree."""
    repo_root = _inside_git_working_tree(output_path)
    if repo_root is None:
        return True

    bar = "!" * 72
    print()
    print(bar)
    print("!!  WARNING: refusing to write transcript inside a git repository  !!")
    print(bar)
    print(f"Target path : {Path(output_path).resolve()}")
    print(f"Git root    : {repo_root}")
    print()
    print("AI session transcripts can contain absolute file paths, secrets")
    print("from files you attached with @filename, and content from unrelated")
    print("sessions on your machine. Committing them to a public repo leaks")
    print("that information.")
    print()
    print("Re-run the script with an output path outside any git working tree,")
    print("e.g.:  python collect_transcripts.py -o ~/ai_transcript.zip")
    print(bar)
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Collect AI session transcripts for lab submission."
    )
    parser.add_argument(
        "--output", "-o",
        default=str(Path.home() / "ai_transcript.zip"),
        help="Output zip path (default: ~/ai_transcript.zip, outside any git repo)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Write even if the output path is inside a git working tree "
             "(NOT recommended; the transcript may contain secrets)",
    )
    args = parser.parse_args()

    if not args.force and not _warn_if_in_git(args.output):
        return

    print("Searching for AI session data on this machine...")
    sessions = discover_sessions()
    display_sessions(sessions)

    if not sessions:
        return

    print()
    prompt = "Enter session number(s) to export (e.g. 1,3 or 1-2), or 'q' to quit: "
    selection = input(prompt).strip()
    if selection.lower() in ("q", "quit", "exit", ""):
        print("No sessions exported.")
        return

    indices = parse_selection(selection, len(sessions))
    if not indices:
        print("No valid sessions selected.")
        return

    export_sessions(sessions, indices, args.output)
    print(f"Upload {args.output} to Blackboard as your AI transcript.")
    print("Do NOT commit the transcript file to a git repository.")


if __name__ == "__main__":
    main()
