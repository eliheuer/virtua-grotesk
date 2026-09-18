# Agent workflows

Codex discovers repository skills in `.agents/skills/`. `AGENTS.md` carries
shared project constraints; each `SKILL.md` carries its specific workflow.
Claude Code uses the same files through `.claude/skills` and `CLAUDE.md`.

| Work | Skill |
| --- | --- |
| Onboarding audit, release readiness, coordinating remaining work | [google-fonts-onboarding](skills/google-fonts-onboarding/SKILL.md) |
| Compiled-font or package QA, coverage and proof evidence | [google-fonts-qa](skills/google-fonts-qa/SKILL.md) |
| Downstream package preview and submission preparation | [google-fonts-packaging](skills/google-fonts-packaging/SKILL.md) |
| Source metrics, kerning, and master compatibility | [font-qa](skills/font-qa/SKILL.md) |

Invoke a skill with `$google-fonts-onboarding` or describe the task naturally.
Skill descriptions identify when to use each workflow; only load supporting
references when they help the task. The onboarding skills' `agents/openai.yaml`
files provide Codex UI labels and starting prompts, not another instruction copy.

Project status and decisions live in [the onboarding checklist](../documentation/google-fonts/README.md).
The [shared procedure](google-fonts-onboarding-checklists.md) is reusable;
[official references](google-fonts-official-reference-map.md) supply specifications.
All command and code paths in these skills are relative to the repository root.

This layout follows [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills)
and [AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
Instructions emphasize clear scope, evidence, and follow-through, consistent with
[the Astra model guidance](https://developers.openai.com/api/docs/guides/latest-model)
checked on 2026-09-09. Model choice remains a Codex task setting; these font
workflows do not require a model-specific config or API key.
