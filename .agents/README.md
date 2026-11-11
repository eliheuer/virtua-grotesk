# Agent files

`AGENTS.md` at the repository root is the guide for every agent. Codex, Claude
Code and OMP read it.

| Directory | Content |
| --- | --- |
| `skills/` | Procedures that an agent loads by name, `build-and-proof`, `font-qa` and `google-fonts-release`. Codex, Claude Code and OMP find them here. |
| `tasks/` | Task contracts for long or unattended runs: goal, acceptance, constraints, and the report to give at the end. |

`.omp/RULES.md` is a link to `AGENTS.md`. OMP gives rules to its subagents,
but not `AGENTS.md`, so the link gives subagents the same rules.

## Run a task with OMP

Use a separate checkout, so that an unattended run cannot change your working
tree:

```sh
git worktree add ../virtua-grotesk-omp main
cd ../virtua-grotesk-omp
omp -p --wait-async --max-time 60m \
  "Do the task in .agents/tasks/glyph-drafts.md for: acute caron circumflex, Regular."
```

Then review the branch, the report and the proof sheets in `out/review/`.
`scripts/check_changes.py` checks the source changes of any run.
