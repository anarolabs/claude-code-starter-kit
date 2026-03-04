# Date grounding hook

## The problem

Claude's training data has a cutoff. Without grounding, it might write `2025-01-15` in a filename when it's actually 2026. This is especially annoying for:
- File naming (date-prefixed documents)
- Meeting notes and logs
- Any temporal reference ("last week", "next month")

## The fix

A hook that runs on every prompt and injects today's date:

```json
// In ~/.claude/settings.json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[SYSTEM] Current date: $(date '+%Y-%m-%d'). Use this for all temporal references.\""
          }
        ]
      }
    ]
  }
}
```

## What it does

Every time you send a message, this hook runs first and tells Claude the current date. Claude sees it as a system message and uses it for all date references in that response.

You never have to think about it - it just works in the background.
