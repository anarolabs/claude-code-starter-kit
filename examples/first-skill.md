# Your first skill (slash command)

## What skills are

Skills are reusable workflows stored as markdown files. Instead of explaining a multi-step process every session, you write it once and invoke it with `/command-name`.

They live in `~/.claude/commands/` and are available in every project.

## Example: a simple meeting prep skill

```markdown
# Meeting prep

Prepare a meeting brief for the person or topic I specify.

## Steps

1. Ask me who the meeting is with and what it's about
2. Check my recent files for any prior notes or context about this person/topic
3. Draft a brief with:
   - Key context (what we last discussed, any open items)
   - My goals for this meeting
   - Questions I should ask
4. Save as YYYY-MM-DD_MEETING_PREP_[NAME].md in the current project's 03-meetings/ folder
```

Save this as `~/.claude/commands/meeting-prep.md` and invoke it with `/meeting-prep`.

## What makes a good skill

- **Repeatable**: You do this workflow at least twice a week
- **Multi-step**: It involves more than one action
- **Consistent**: The steps matter and you want them done the same way each time

## What doesn't need a skill

- One-off tasks ("summarise this email")
- Simple questions ("what does this function do?")
- Anything you'd describe differently each time

## Advanced: skills can be sophisticated

Skills can include:
- Multiple phases with checkpoints
- Calls to external scripts (email, calendar, sheets)
- Decision gates that ask you before proceeding
- Context loading from specific files

Start simple. You can always make them more sophisticated later.
