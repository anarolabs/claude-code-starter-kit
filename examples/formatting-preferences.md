# Formatting preferences

These are the small things that add up. Without them, you correct Claude on the same things every session.

## Example rules (from a real setup)

```markdown
## Formatting rules

- Use British English spelling (colour, organised, behaviour)
- Use sentence case for all headings (capitalize only the first word)
  - Correct: "What delivery options do you offer?"
  - Incorrect: "What Delivery Options Do You Offer?"
- Don't use em dashes (-). Use spaced hyphens instead.
- Don't use emojis unless explicitly requested
- Don't use horizontal rules (---) between sections - let headings create separation
```

## Why these matter

- **British English**: Without this, Claude defaults to American English. If you write "colour" and Claude writes "color" in the same document, it looks sloppy.
- **Sentence case**: Claude loves Title Casing Every Word. It looks like a PowerPoint from 2008.
- **Em dashes**: They render inconsistently across platforms (Google Docs, Notion, markdown). Spaced hyphens are universal.
- **Emojis**: Claude sprinkles them liberally by default. Fine in chat, awful in professional documents.

## How to add your own

Think about the last few times Claude's formatting annoyed you. That's your list. Add rules when you catch yourself correcting the same thing twice.
