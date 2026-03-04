# File organization

## Why it matters

Without conventions, Claude creates files with inconsistent names in random locations. You waste time renaming and moving things. Set the rules once, never think about it again.

## Example convention

```markdown
## File naming
- Format: YYYY-MM-DD_DESCRIPTION.md
- Example: 2026-03-04_MEETING_PREP_CLIENT_X.md
- Always use ISO date format at the start for chronological sorting
- Use UPPERCASE with underscores for the description portion

## Directory structure
Use numbered prefixes for project folders:
- 01-context/ - Foundation documents and strategic context
- 02-research/ - Research, discovery, and analysis
- 03-meetings/ - Meeting prep and notes
- 04-agents/ - Agent configurations (if using agents)
- archive/ - Deprecated or superseded documents

## Project root
All project files live in: ~/Documents/Claude Code/[project-name]/
```

## The key insight

Date-prefixed files sort chronologically in any file browser. When you open a folder, the most recent files are at the bottom (or top, depending on sort). No more hunting for "which version is latest?"
