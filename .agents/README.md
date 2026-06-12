# Agent Skills

This directory contains reusable agent skills for font development work.
Skills under `skills/` should avoid project-only assumptions when possible so
they can be copied into another font repository and adapted with small edits.

This is the **single canonical location** for skills, shared across AI tools:
`.claude/skills` is a symlink to `skills/` so Claude Code discovers them too.
Edit skills here only — do not create copies under `.claude/`. Each
`SKILL.md` starts with YAML frontmatter (`name`, `description`) which Claude
Code requires for skill registration; keep it when adding new skills.

For Google Fonts onboarding, start with:

- `skills/google-fonts-onboarding/SKILL.md`
- `skills/google-fonts-qa/SKILL.md`
- `skills/google-fonts-packaging/SKILL.md`
- `skills/google-fonts-nonlatin-drawing/SKILL.md`
- `google-fonts-onboarding-checklists.md`
- `google-fonts-official-reference-map.md`
