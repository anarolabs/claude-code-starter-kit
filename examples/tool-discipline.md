# Tool discipline

## The problem

Claude Code has built-in tools that are purpose-built and give clean output:
- **Read** - reads files with line numbers
- **Grep** - searches file contents with regex
- **Glob** - finds files by pattern
- **Edit** - makes precise edits to files

But Claude sometimes falls back to bash equivalents (`cat`, `grep`, `ls`, `find`). These work, but:
- They trigger permission prompts you have to approve
- The output is raw and harder to review
- They bypass the structured tool output that makes reviewing changes easier

## The fix

Add deny rules in `~/.claude/settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Bash(cat:*)",
      "Bash(echo:*)",
      "Bash(grep:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(ls:*)",
      "Bash(find:*)"
    ]
  }
}
```

When Claude tries to use `cat` to read a file, it gets blocked and automatically falls back to the Read tool instead. You get cleaner output and fewer permission prompts.

## What to allow

Pre-approve tools you trust to reduce permission fatigue:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Grep",
      "Glob",
      "Bash(git:*)",
      "Bash(python3:*)",
      "Bash(date:*)"
    ]
  }
}
```

Start conservative. Add permissions as you notice things you always approve.
