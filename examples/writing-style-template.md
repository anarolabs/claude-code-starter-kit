# Writing style guide (template)

A writing style guide is the highest-leverage file in your Claude Code setup. It's the difference between Claude writing *for* you and Claude writing *as* you.

## What goes in it

### 1. Voice characteristics
Describe how you sound in 3-4 adjectives, then show what that means in practice:

```markdown
## Tone and voice

- Direct, not corporate. Confident, not arrogant.
- Lead with the answer, then give context
- Use specific numbers over vague quantities
- Make declarative statements, don't hedge
```

### 2. Show, don't tell (example pairs)
The most effective way to teach Claude your voice. For each pattern, show what you don't want and what you do want:

```markdown
**Answer first, context second**
- Yes: "My day rate is 1,200. Two ways to structure it..."
- No: "So I've been doing this for a while and at my last company we..."

**Specific over vague**
- Yes: "25 managers enable 150+ employees"
- No: "Managers enable many employees"

**Declarative over hedging**
- Yes: "The magic is in cohorts, not self-serve"
- No: "I think cohorts might be better in some ways"
```

### 3. Anti-patterns (things you never want)
Be explicit about what Claude should never write:

```markdown
## Anti-patterns

- Never start with "In today's fast-paced world" or similar filler
- Never use "Let's dive in" or "Here's what you need to know"
- Never cite statistics without a source link
- Never write "most people think X" without evidence
- Never use "Let that sink in" or "Read that again"
```

### 4. Document-type rules (optional but powerful)
Different rules for different contexts:

```markdown
## Strategic memos
- Put operating principles near the top, before detailed sections
- Break up paragraphs every 2-3 sentences
- Add flexibility caveats after presenting targets

## Emails
- Maximum 3 paragraphs for cold outreach
- Always end with a specific next step, not "let me know"
```

## How to build yours

Start with 3 "don't write X, write Y" pairs from your own writing. That alone gets you 70% of the way. Add more as you notice Claude getting your voice wrong.

The goal is that when Claude drafts something, you're *editing* it, not *rewriting* it.
