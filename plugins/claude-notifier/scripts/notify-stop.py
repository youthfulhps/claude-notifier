#!/usr/bin/env python3
"""
Stop hook: Sends a macOS system notification when Claude finishes a response.
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

TERM_PROGRAM_MAP = {
    "WarpTerminal":  "Warp",
    "iTerm.app":     "iTerm",
    "Apple_Terminal": "Terminal",
    "vscode":        "Cursor",
    "ghostty":       "Ghostty",
    "Hyper":         "Hyper",
}

def detect_app_name():
    term = os.environ.get("TERM_PROGRAM", "")
    return TERM_PROGRAM_MAP.get(term)

try:
    data = json.load(sys.stdin)
    msg = data.get("last_assistant_message", "") or "Task complete"
    if len(msg) > 100:
        msg = msg[:97] + "..."
    cwd = data.get("cwd", "")
    project = Path(cwd).name or "Claude Code"
except Exception:
    msg = "Task complete"
    cwd = ""
    project = "Claude Code"

title = f"Claude Code — {project}"
app_name = detect_app_name()

if shutil.which("terminal-notifier") and app_name:
    subprocess.run([
        "terminal-notifier",
        "-title", title,
        "-message", msg,
        "-subtitle", "Task complete",
        "-sound", "Glass",
        "-execute", f'/usr/bin/open -a "{app_name}"',
    ])
else:
    script = (
        f"display notification {json.dumps(msg, ensure_ascii=False)} "
        f"with title {json.dumps(title, ensure_ascii=False)} "
        f'subtitle "Task complete" '
        f'sound name "Glass"'
    )
    subprocess.run(["osascript", "-e", script])
