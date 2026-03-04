# Memory system

## The three layers

Claude Code has a three-layer memory system. Each layer serves a different purpose:

### Layer 1: Global preferences (`~/.claude/CLAUDE.md`)
- **Always loaded** in every session, every project
- Put your universal rules here: formatting, language, tone, file conventions
- This is your "operating system" - the rules that apply everywhere

### Layer 2: Project-specific instructions (`[project]/CLAUDE.md`)
- Loaded when you're working inside that project directory
- Put project-specific context here: what the project is, key files, workflows
- Example: your EstateMate project has different context than your consulting work

### Layer 3: Auto-memory (`~/.claude/memory/`)
- Claude saves things it learns from working with you
- When you say "remember that I always want X", it writes to MEMORY.md
- When you say "forget that rule about Y", it removes it
- Also captures patterns automatically: script quirks, contact details, things that waste time when forgotten

## How memory grows

**Explicitly**: Tell Claude "remember this for next time" and it saves it.

**Implicitly**: When you correct Claude twice on the same thing, it may save the pattern.

**By editing**: You can directly edit `~/.claude/memory/MEMORY.md` or create topic files like `debugging.md`, `client-contacts.md`.

## The compound effect

Session 1: You correct Claude on 10 things.
Session 5: You correct it on 3 things.
Session 20: It feels like it already knows you.

That's the payoff. Every correction is an investment in future sessions.
