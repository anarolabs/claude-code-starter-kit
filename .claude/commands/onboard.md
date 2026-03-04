# Claude Code onboarding

Walk the user through setting up their Claude Code preferences step by step. This is an interactive onboarding - present each category, explain what it does, show an example from a real setup, and let the user decide what to adopt.

## How this works

You will go through 7 preference categories. For each one:
1. **Explain** what the category does and why it matters (1-2 sentences)
2. **Show the example** from the `examples/` folder in this repo
3. **Ask** if they want to adopt it as-is, modify it, or skip it
4. Collect their choices and build their config files at the end

**Important**: Use AskUserQuestion for each category. Don't rush - let the user think about each one.

---

## Phase 1: Date grounding

**Why it matters**: Claude's training data has a cutoff date. Without grounding, it can get the current year wrong in filenames, references, and temporal reasoning. This hook injects today's date into every prompt automatically.

**Show the user**: Read `examples/hooks/date-hook-example.md` and display it.

Ask: "Do you want to set up automatic date grounding? This ensures Claude always knows today's date."
- Yes, set it up (Recommended)
- Skip for now

If yes, note this for the settings.json output.

---

## Phase 2: Formatting and language preferences

**Why it matters**: Without these, Claude defaults to American English, Title Case Headings, em dashes, and liberal emoji use. These small things add up - you end up correcting the same things every session.

**Show the user**: Read `examples/formatting-preferences.md` and display the example rules.

Ask the user to pick which formatting rules they want (multi-select):
- British English spelling
- Sentence case headings (not Title Case)
- No em dashes (use spaced hyphens instead)
- No emojis unless explicitly requested
- No horizontal rules (---) between sections

Then ask: "Any other formatting preferences you want to add? Things you find yourself correcting often?"

Collect their response as free text.

---

## Phase 3: Writing style and tone of voice

**Why it matters**: This is the highest-leverage preference. Without a style guide, Claude writes in a generic, corporate-sounding voice. A good style guide means you stop rewriting Claude's output and start editing it instead.

**Show the user**: Read `examples/writing-style-template.md` and display it.

Walk them through building their own style by asking these questions one at a time:

1. "How would you describe your writing voice in 3-4 adjectives? (e.g., direct, warm, technical, casual)"

2. "Give me an example of something you'd NEVER write - a sentence or phrase that sounds wrong to you."

3. "Give me an example of something that sounds like YOU - a sentence from an email or doc you've written that captures your voice."

4. "Any specific anti-patterns? Things Claude (or AI in general) tends to write that you hate? Common ones: 'Let's dive in', 'In today's fast-paced world', 'Here's what you need to know', fake statistics."

Use their answers to draft a WRITING_STYLE_GUIDE.md file. Show it to them for approval before saving.

---

## Phase 4: File organization

**Why it matters**: When Claude creates files, it needs to know your naming conventions. Without this, you get inconsistent filenames and files scattered in random locations.

**Show the user**: Read `examples/file-organization.md` and display the example conventions.

Ask: "How do you want files named and organized?"
- Date-prefixed files (2026-03-04_DESCRIPTION.md) (Recommended)
- Descriptive names only (no dates)
- Custom convention

Ask: "Where should Claude save project files by default?"
- Let them specify their preferred project root directory

---

## Phase 5: Memory system

**Why it matters**: Claude Code can remember things across sessions. When you correct it ("I told you, always use British English"), it can save that so you never have to say it again. But it needs to be set up.

**Show the user**: Read `examples/memory-system.md` and explain the three layers.

Ask: "Do you want to enable auto-memory? Claude will save patterns it learns from working with you."
- Yes, set it up (Recommended)
- Skip for now

If yes, create the initial memory directory and seed file.

---

## Phase 6: Tool discipline

**Why it matters**: By default, Claude sometimes uses bash commands (cat, grep, ls) when it has better built-in tools (Read, Grep, Glob). Setting up deny rules forces it to use the right tools, which gives you better output and cleaner permission prompts.

**Show the user**: Read `examples/tool-discipline.md` and display the concept.

Ask: "Do you want to set up tool discipline rules? This forces Claude to use its built-in tools instead of bash equivalents."
- Yes, set it up (Recommended)
- Skip for now

---

## Phase 7: Google Workspace connection

**Why it matters**: With Google Workspace connected, Claude can read your email, search your Drive, read and create Docs, and work with Sheets - all from the conversation. No browser switching.

**Pre-requisite**: Your admin should have given you a service account JSON key file. If you don't have one, skip this step and ask your admin to set one up.

Ask: "Do you have a Google service account JSON key file from your admin?"
- Yes, I have the file
- No, skip for now

If yes:

1. Ask for the path to their JSON key file
2. Ask for their Google Workspace email address
3. Run the setup script:

```bash
bash scripts/setup_google.sh /path/to/their-key.json their-email@domain.com
```

This will:
- Copy the key to `~/.config/claude-code/google-service-account.json`
- Set secure permissions (600)
- Install Google API dependencies
- Test the connection against Gmail, Drive, Sheets, and Calendar

If all tests pass, tell them: "Google Workspace is connected. Claude can now read your email, access your Drive, and work with your Docs and Sheets."

If any tests fail, check:
- Is the email address correct?
- Has the admin authorized domain-wide delegation for this service account?
- Are the APIs enabled in Google Cloud Console?

---

## Phase 8: Building your first skill

**Why it matters**: Skills (slash commands) are reusable workflows. Instead of explaining a multi-step process every time, you write it once as a markdown file and invoke it with `/command-name`.

**Show the user**: Read `examples/first-skill.md` and display the example.

Don't build a skill now - just explain the concept and where they live (`~/.claude/commands/`).

Ask: "What's a workflow you repeat often that you'd want to automate? Just describe it briefly - we can build it together in a future session."

Save their answer to their CLAUDE.md as a reminder.

---

## Phase 9: Generate and install

Now generate all the config files based on the user's choices:

1. **`~/.claude/CLAUDE.md`** - Global preferences file with all their chosen rules
2. **`WRITING_STYLE_GUIDE.md`** - In their project root (or a location they specify)
3. **`~/.claude/settings.json`** - With hooks (date grounding) and deny rules (tool discipline) if selected
4. **`~/.claude/memory/MEMORY.md`** - Seed file if memory was enabled

For each file:
- Show the full content before writing
- Ask for confirmation
- Explain where it's saved and what it does

**After installation**, tell the user:

"Your Claude Code setup is ready. Here's what to know going forward:

- **CLAUDE.md** loads automatically every session. Edit it anytime to add new rules.
- **Writing style guide** is referenced from your CLAUDE.md. Update it when you notice Claude getting your voice wrong.
- **Memory** grows automatically. You can also explicitly say 'remember this' or 'forget that rule' in any session.
- **Settings** control permissions and hooks. You'll rarely need to edit these directly.

The best way to improve your setup: when you catch yourself correcting Claude, add the correction to your CLAUDE.md. After a few sessions, it'll feel like it already knows you."
