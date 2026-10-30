# Agent guidance

Virtua Grotesk is an OFL variable font. Start with the user's task, inspect the
working tree, and preserve unrelated work. Use current files and evidence over
dated prose. Complete authorized reversible work without repeated permission
questions; reuse named approvals and preserve unresolved human decisions.

## Find the right context

- Drawing, spacing, components or curves: [design workflow](design/README.md),
  then `.venv/bin/python scripts/design_context.py --glyph <name> --operation <operation>`.
  Read its applicable construction rules, corrections, exceptions and live source
  facts. The packet is context, not authorization. Save JSON guards before edits.
- Current review and stopped work: `make design-status`, then the named case in
  [design/reviews/current.json](design/reviews/current.json). Historical grants
  and queues do not restart work. Record feedback before the next edit.
- A–Z/a–z: also read [Latin worklog](design/reviews/latin-worklog.md); OPEN
  decisions belong to Eli. Append measured decisions there.
- Image references: use `anchor-sheet-glyphs` for calibrated sheets or
  `glyph-ai-harness` for image generation/tracing. Follow their operational guides.
- Release scope: [onboarding checklist](documentation/google-fonts/README.md)
  and `google-fonts-onboarding`; binary/package checks: `google-fonts-qa`;
  downstream preview: `google-fonts-packaging`; source checks: `font-qa`.
- Interactive design review: `render-specimen`, `make proof-web`, and
  [web proof guide](agent-proofs/app/README.md). Preserve the accepted layout.

Shared procedural skills live in `.agents/skills/`; `CLAUDE.md` and
`.claude/skills` are compatibility routes. Edit canonical files. Design knowledge
belongs in `design/`, not copied into each skill. Do not read every skill or the
whole review archive. [DESIGN.md](DESIGN.md) is the human-readable topic router.

## Source safety

Active inputs: `sources/VirtuaGrotesk.designspace`, Regular and Bold UFOs,
`sources/config.yaml`. `sources/archive/` is historical. The weight axis is
400–700. Shared metrics/grid/colors are in `design/system/contract.json`.
New machine drafts use 8 units; preserve human optical corrections on 2.

Before drawing, identify exact glyphs, masters and purpose; reuse existing
approval for that scope, otherwise obtain it. Candidate permission is distinct
from active application. Preserve a before snapshot, inspect current colors and
hashes, and recheck the context packet immediately before writing. Stop for a
broader scope or unresolved human decision; continue independent work.

Only green is frozen by default, including composites. A green change requires
explicit named permission. Check recursive donors and consumers so a donor edit
does not indirectly change a protected glyph. Red is replaceable within scope;
orange/yellow retain useful drawing; blue/pink are composite repair states.
Purple means AI drawing awaiting human review, not approval or reference status.
Use Eli's purple convention for newly AI-drawn work; never assign green. Unknown
colors require classification. Preserve reserved human edits regardless of color.

Both masters must have corresponding contour/point/component structure. Edit
GLIF XML and plists surgically in existing style (tabs, double quotes, no space
before `/>`, x/y/type/smooth attribute order). Never use whole-UFO `font.save()`.
Register new glyphs in contents.plist and public.glyphOrder in both masters.

## Verification and handoff

Use `.venv/bin/python`. Follow [design verification](design/system/verification.md)
and [QA](documentation/qa.md): source checks, build, compiled shaping, affected
rendered proofs and preflight. After curve edits run `curve_lint.py --joins` and
inspect large glyphs plus reading-size context. Inspect actual rendered output;
command success is not visual review. Human approval and release readiness remain
separate. Do not exclude Fontspector checks just to pass.

`make help` lists commands. `make review` is Diffenator3 QA; `make proof` is the
DesignBot PDF; `make specimen` is unimplemented. Preflight checks artifact presence,
and skeleton tolerates QA failures; neither proves release readiness.
When asked to open a font, use `runebender-serve <designspace-or-ufo> --open` and
leave it running. Use the native editor only when explicitly requested.

Keep updates concise and scope-specific. Preserve proposed/verified/approved/
published distinctions and evidence hashes in handoffs. Review-only means no
edits; preparation does not authorize public messages or publication. Use plain
commit messages without agent credit or generated-by trailers.
