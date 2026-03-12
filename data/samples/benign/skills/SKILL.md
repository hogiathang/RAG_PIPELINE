---
name: osctrl-desktop-automation
description: Use when automating desktop interactions via OSCTRL CLI - mouse, keyboard, screen capture, window management. ALWAYS get context before mouse operations.
---

# OSCTRL Desktop Automation Skill

## When to Use

- Automating mouse clicks, movements, drags
- Typing text or pressing keys programmatically
- Managing windows (focus, move, resize, minimize/maximize)
- Taking screenshots for verification
- Reading/writing clipboard
- Launching or listing processes

## Critical Rule

**ALWAYS call `osctrl context` before any mouse operation.** Never click blindly.

## Quick Reference

| Command                                 | Purpose                                        |
| --------------------------------------- | ---------------------------------------------- |
| `osctrl context`                        | Get screen size, mouse position, active window |
| `osctrl mouse move <x> <y>`             | Move cursor                                    |
| `osctrl mouse click`                    | Left click                                     |
| `osctrl keyboard type <text>`           | Type text                                      |
| `osctrl keyboard hotkey <keys...>`      | Key combination (ctrl c, alt f4)               |
| `osctrl screen capture --output <path>` | Screenshot                                     |
| `osctrl window focus <title>`           | Focus window                                   |

## Workflow

```
1. osctrl context              # Get state
2. Validate coordinates        # Within screen bounds
3. osctrl window focus <app>   # Ensure correct window
4. osctrl mouse move <x> <y>   # Position cursor
5. osctrl mouse click          # Execute action
6. osctrl screen capture       # Verify result
```

## See Also

Full instructions available in `docs/ai-instructions/` for:

- Claude Code (CLAUDE.md)
- Cursor (.cursorrules)
- OpenAI Codex
- Gemini CLI
