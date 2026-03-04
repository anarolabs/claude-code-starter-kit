# Ways of working (project CLAUDE.md pattern)

## The concept

Your global `~/.claude/CLAUDE.md` holds universal rules. But each project gets its own `CLAUDE.md` at the project root with project-specific context, workflows, and conventions.

When you `cd` into a project folder, Claude automatically loads that project's CLAUDE.md on top of your global one.

## Example: a consulting project

```markdown
# Client project - Acme Corp

## Project overview
Fractional CX engagement, 16hrs/week. Focus on workforce management and BPO operations.

## Key contacts
- Sarah (VP CX): sarah@acme.com
- Mike (WFM lead): mike@acme.com

## Workflows

### Context loading
When starting work on this project, load:
- 01-context/STATUS.md for current state
- 03-meetings/ for recent meeting notes

### Update skill
/acme-update runs a full sync:
1. Check Gmail for recent client emails
2. Check meeting notes for new items
3. Update STATUS.md with any changes
4. Surface action items

### Deliverables
All client-facing documents follow:
- Company report template in 02-research/templates/
- Writing style: professional but direct, no jargon
- Always include next steps with clear ownership
```

## Example: a product project

```markdown
# EstateMate

## What this is
Real estate management SaaS platform.

## Key files
- 01-context/PRODUCT_SPEC.pdf - Full product specification
- 05-codebase/ - Application source code

## Workflows
### Feature improvement
/em-improve - File a structured product improvement with rationale and impact assessment

### Project update
/estatemate-update - Scan for changes, update dashboards, surface decisions needed
```

## The payoff

When you start a session inside a project folder, Claude already knows:
- What the project is
- Who the key people are
- What workflows to follow
- Where files should go

No setup, no context-setting. Just start working.
