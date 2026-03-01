# claude-notifier

A Claude Code plugin that sends macOS system notifications on task completion and events.

> **macOS only.** This is a prototype.

## Requirements

- macOS
- Python 3 (pre-installed on macOS)
- Claude Code with plugin support

## Features

- System notification when Claude finishes a response
- Notifications for events like permission prompts and idle state
- Project name in notification title (`Claude Code — my-project`)
- (Optional) Click notification to focus the terminal app

## Installation

**1. Add the marketplace**

```bash
claude plugin marketplace add youthfulhps/claude-notifier
```

**2. Install the plugin**

```bash
claude plugin install claude-notifier@claude-notifier
```

The plugin loads automatically in every Claude Code session.

To uninstall:

```bash
claude plugin uninstall claude-notifier@claude-notifier
```

## Permissions

**Notification permission** — macOS will prompt you automatically on first run. Just allow it.

If notifications don't appear, check manually:
> System Settings → Notifications → `Script Editor` → Allow notifications

## Click to Focus (Optional)

Clicking a notification brings the terminal app to the foreground.

### 1. Install terminal-notifier

```bash
brew install terminal-notifier
```

### 2. Grant Accessibility Permission

> System Settings → Privacy & Security → Accessibility

Click `+` and add your terminal-notifier app path, then enable the toggle. To find the exact path:

```bash
brew info terminal-notifier
```

The path looks like:

```
/opt/homebrew/Cellar/terminal-notifier/<version>/terminal-notifier.app
```

### Supported Terminals

| Terminal | `$TERM_PROGRAM` |
|----------|----------------|
| Warp | `WarpTerminal` |
| iTerm2 | `iTerm.app` |
| Terminal.app | `Apple_Terminal` |
| Ghostty | `ghostty` |
| Hyper | `Hyper` |
| VS Code / Cursor | `vscode` |

### VS Code vs Cursor

VS Code and Cursor share the same `$TERM_PROGRAM` value (`vscode`).
Edit `TERM_PROGRAM_MAP` in `scripts/notify-stop.py` and `scripts/notify-event.py` to specify which one you use:

```python
TERM_PROGRAM_MAP = {
    ...
    "vscode": "Cursor",  # or "Visual Studio Code"
}
```

Terminals not listed above will still receive notifications, but click-to-focus will not work.

## How It Works

The plugin registers two Claude Code hooks:

| Hook | Trigger | Script |
|------|---------|--------|
| `Stop` | Claude finishes a response | `notify-stop.py` |
| `Notification` | Permission prompt, idle, auth, elicitation | `notify-event.py` |

Each script reads event data from stdin (JSON), extracts the current project name from `cwd`, and delivers a notification via:

- **`osascript`** (default) — uses the macOS built-in notification system via AppleScript
- **`terminal-notifier`** (if installed) — adds click-to-focus support via `-execute`

### Notification Events

| Event | Subtitle |
|-------|---------|
| Response complete (`Stop`) | Task complete |
| `permission_prompt` | Permission request |
| `idle_prompt` | Waiting for input |
| `auth_success` | Authenticated |
| `elicitation_dialog` | Information request |

### Setup Summary

| Setup | Notifications | Click to Focus |
|-------|--------------|----------------|
| Default (no extra setup) | ✅ | ❌ |
| terminal-notifier + Accessibility permission | ✅ | ✅ |

## License

MIT
