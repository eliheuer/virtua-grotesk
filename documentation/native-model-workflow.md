# Native Runebender + local model + coding agent

This workflow uses the actual native editor and its Agent Proof view. The local
model makes a proposal; the coding agent coordinates inspection and bounded edits;
Eli judges and corrects the result. Keep model trials in a scratch font. Neither
model scores nor green training examples grant permission to edit a real glyph.

## Portable model setup

From this repository, on Linux or macOS with Python3.11+:

```sh
python3 -m venv .venv-repair
. .venv-repair/bin/activate
python -m pip install 'torch>=2.6,<3'
python scripts/propose_arabic_repair.py --out out/arabic-repair-demo
```

PyTorch is the large dependency; the bundled model is only148KiB. No GPU, model
service, training corpus, or font-garden-lab checkout is required for inference.
The tested macOS runtime was PyTorch2.13.0. Linux execution has not yet been
verified; compare proposal.json to models/arabic-repair-hour-v1/expected-sample.json
for the bundled sample. Different runtimes may differ near rounding thresholds;
report differences rather than silently accepting them. No training starts here.
The runner refuses existing output directories and writes only beneath out/.
It produces a new Review.ufo with input/model glyphs, JSON proposal and receipt.

Use a built native Runebender executable (replace RUNEBENDER with its absolute
path; do not assume an old installed binary is current):

```sh
RUNEBENDER=/absolute/path/to/runebender
"$RUNEBENDER" "$PWD/out/arabic-repair-demo/Review.ufo"
```

## Agent connection and version requirements

Configure the harness's MCP bridge to launch that same executable with arguments
`mcp --live`. This is a stdio MCP server, not an HTTP endpoint. Runebender and the
agent must run on the same machine/user session for its local editor sockets.
For direct Codex integration Runebender provides `mcp --install codex`; that does
not automatically configure a Pi harness. Pi needs an MCP-capable extension or
bridge. Its exact configuration depends on the installed Pi extension; no Pi
configuration has been verified here. The model can also be invoked as a normal
shell tool from Pi using the command above.

Check tools/list before promising the full demo: editor_sessions, editor_connect,
project_info, editor_context, read_glyph, design_context, editor_open_glyph,
editor_select_points, editor_review, review_proof, agent_apply and agent_history.
Missing tools mean the native editor/bridge needs updating.

The required hooks are in Runebender commit
`b1ad474` (Expose native point selection and review controls over MCP).
Build a revision containing that commit; check `git merge-base --is-ancestor
b1ad474 HEAD` in the Runebender checkout. Publication of that commit must be
confirmed separately from this Virtua repository. Pulling Virtua alone cannot
update Runebender. Do not copy a macOS executable to Linux. Follow Runebender's
build instructions and use the same binary for both editor and MCP process.

## Copy-ready first request to the agent

> Read AGENTS.md and documentation/native-model-workflow.md. Verify the bundled
> checkpoint hash and run the sample inference, without training. Compare the
> result against expected-sample.json; report any difference. Open only the new
> scratch Review.ufo in native Runebender. Connect to its exact MCP session,
> verify the required tools, and show the input versus model output in native
> Agent Proof. Pin the input as Before, then apply model coordinates only to
> that scratch input glyph with current epoch/revision guards. Keep the original
> model glyph as an on-disk copy. Capture review_proof and inspect the image.
> Do not edit Virtua sources, assign grades, save the editor document, or start
> training. Pause for my feedback before further edits. If Pi has no MCP bridge,
> report that setup gap instead of pretending shell inference controls the editor.

Sample verification after inference:

```sh
python -c "import json; from pathlib import Path; assert json.loads(Path('out/arabic-repair-demo/proposal.json').read_text()) == json.loads(Path('models/arabic-repair-hour-v1/expected-sample.json').read_text()); print('Exact sample match')"
```


## One glyph at a time

1. Discover sessions and connect to the exact scratch path, never the first window
   by assumption. Read project_info and editor_context for stable source identity
   and document epoch. Read design_context and the scoped Virtua design packet.
2. Open the chosen glyph. editor_review with action=pin_before captures Before;
   each UI operation requires a freshly read expected_context_revision.
3. Read the current live points. Build an inference JSON like sample.json: input
   contains Regular glyph, group (a descriptive inference label is sufficient),
   provenance hash, advance and contours; editable_mask has one0/1 value per point
   in contour order. Keep GLIF offcurve points without a type attribute. Preserve
   human optical coordinates; unsupported coordinates are rejected, not clipped.
   Select a bounded region, considering both stroke boundaries. No target data is
   needed for inference. Run propose_arabic_repair.py with --input and a new --out.
4. Validate topology, locked points and current revision. Use editor_review/edit,
   then editor_select_points with canonical point IDs from read_glyph to show
   native yellow selection. Map proposed coordinates to those exact IDs. Apply
   only the named authorized scratch edit with agent_apply, explicit source,
   document epoch and glyph revision. Never treat a new read as permission to
   rebase a stale proposal. Keep operation receipts for idempotent retries/undo.
5. editor_review/compare or before/after shows the native proof. review_proof
   returns an image of that same comparison and available reference drawings.
   Synthetic scratch names are unencoded, so reference cards may say no Unicode;
   compare input/model directly rather than inventing aliases. A real glyph's
   contextual/shaping proof remains a separate verification requirement.
6. Stop for human review. Model output is experimental, not green. Do not save,
   install a real-font proposal, or change grading without named authorization.

## Human/agent handoff

One editor, alternating control—not concurrent writes to the same glyph. On human
takeover, stop mutations and cancel queued edits. When Eli says to continue, reread
the live unsaved geometry, selection, epoch and revisions; discard old proposals.
Saving is Eli's choice and is not required for live MCP reads. Capture exact before
and corrected-after bytes with the explanation of intent. Add to training only
with explicit approval/green grading and family-aware split checks.

Keep source files and protected recursive donors unchanged during scratch demos.
Leave editor windows and unrelated work alone. Persist small receipts and approved
lessons; leave generated UFOs, checkpoints from intermediate runs, and screenshots
in ignored out/. A shared README is not authorization for unattended drawing.
