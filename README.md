# Claude Code starter kit

A care package for getting the most out of Claude Code. Instead of figuring it out by trial and error, this repo walks you through setting up the preferences and patterns that actually matter.

## What's inside

```
claude-code-starter-kit/
├── .claude/commands/
│   └── onboard.md          # Interactive onboarding skill
├── examples/
│   ├── hooks/
│   │   └── date-hook-example.md
│   ├── formatting-preferences.md
│   ├── writing-style-template.md
│   ├── file-organization.md
│   ├── memory-system.md
│   ├── tool-discipline.md
│   ├── first-skill.md
│   └── ways-of-working.md
└── README.md
```

## How to use it

1. Clone this repo somewhere on your machine
2. Open Claude Code inside the repo folder
3. Run `/onboard`

The onboarding skill walks you through 7 preference categories:

1. **Date grounding** - so Claude always knows today's date
2. **Formatting** - British English, heading style, em dashes, emojis
3. **Writing style** - teach Claude your voice with example pairs
4. **File organization** - naming conventions and project structure
5. **Memory** - how Claude remembers things across sessions
6. **Tool discipline** - cleaner output, fewer permission prompts
7. **Your first skill** - identify a workflow to automate

At the end, it generates and installs your config files.

## What you'll end up with

- `~/.claude/CLAUDE.md` - your global preferences (loaded every session)
- `WRITING_STYLE_GUIDE.md` - your voice and tone definition
- `~/.claude/settings.json` - hooks and permissions
- `~/.claude/memory/MEMORY.md` - seed file for auto-memory

## After onboarding

The `examples/` folder is your reference library. Come back to it when you want to:
- Add a new formatting rule
- Refine your writing style guide
- Set up a project-specific CLAUDE.md (see `ways-of-working.md`)
- Build your first custom skill

## The compound effect

Session 1: you correct Claude on 10 things.
Session 5: you correct it on 3 things.
Session 20: it feels like it already knows you.

Every correction is an investment. This repo gives you a head start.
