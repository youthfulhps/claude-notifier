#!/usr/bin/env python3
"""
Notification hook: Sends macOS system notifications for Claude Code events (permission prompts, idle, etc.).
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

TERM_PROGRAM_MAP = {
    "WarpTerminal":   "Warp",
    "iTerm.app":      "iTerm",
    "Apple_Terminal":  "Terminal",
    "vscode":         "Cursor",
    "ghostty":        "Ghostty",
    "Hyper":          "Hyper",
}

TYPE_LABELS = {
    "permission_prompt":  ("Permission request", "Ping"),
    "idle_prompt":        ("Waiting for input",  "Tink"),
    "auth_success":       ("Authenticated",       "Glass"),
    "elicitation_dialog": ("Information request", "Ping"),
}

def detect_app_name():
    term = os.environ.get("TERM_PROGRAM", "")
    return TERM_PROGRAM_MAP.get(term)

try:
    data = json.load(sys.stdin)
    event_type = data.get("notification_type", "")
    subtitle, sound = TYPE_LABELS.get(event_type, ("Notification", "Ping"))
    msg = data.get("message", "You have a notification")
    if len(msg) > 100:
        msg = msg[:97] + "..."
    cwd = data.get("cwd", "")
    project = Path(cwd).name or "Claude Code"
except Exception:
    subtitle, sound, msg = "Notification", "Ping", "You have a notification"
    cwd = ""
    project = "Claude Code"

title = f"Claude Code — {project}"
app_name = detect_app_name()

if shutil.which("terminal-notifier") and app_name:
    subprocess.run([
        "terminal-notifier",
        "-title", title,
        "-message", msg,
        "-subtitle", subtitle,
        "-sound", sound,
        "-execute", f'/usr/bin/open -a "{app_name}"',
    ])
else:
    script = (
        f"display notification {json.dumps(msg, ensure_ascii=False)} "
        f"with title {json.dumps(title, ensure_ascii=False)} "
        f"subtitle {json.dumps(subtitle, ensure_ascii=False)} "
        f'sound name "{sound}"'
    )
    subprocess.run(["osascript", "-e", script])
