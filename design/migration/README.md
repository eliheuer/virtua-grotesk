# Design context transition — 2026-10-29

Correction metadata now lives in design/corrections, apart from the proof app.
Review source/proof artifacts moved intact to design/reviews. Shared rules have
one owner under system, constructions, writing-systems or glyphs; skills route
to them. `design_context.py` retrieves relevant evidence and emits input hashes.

The blog's 8-unit structural grid, 2-unit optical corrections and descriptive
popcount are explicit in the contract. They describe geometry, not approval or
training eligibility. See [Eli's article](https://elih.net/blog/virtua-grotesk/).
The narrow entry points and on-demand evidence follow the progressive disclosure
approach described in [OpenAI's skills guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
Retrieval regression tests exercise actual design failures: Seen articulation,
Zayin versus hamza handles, final Yeh intent and rejected at drafts.

Compatibility routes preserve old paths. Frozen review artifacts and receipts
retain their bytes, including historical absolute paths; use the prefix map in
[legacy-paths.json](legacy-paths.json) for external consumers. Local external fonts
remain in reference-fonts. The current rejected Seen v4 proof was copied from out
into the case so a fresh checkout can reopen it without the old scratch directory.

No source drawings are changed by this migration. Source guards detect edits
between preparation and application; they are not a filesystem lock. Agents must
still inspect changes and preserve concurrent editor saves. This is context and
provenance infrastructure, not model training. The companion font-garden-lab
extractor is outside this repository and has not been migrated or revalidated.
Old arbitrary absolute paths inside archived scripts may still require deliberate
historical reproduction; only maintained entry points are promised portable.

The [QA-chat handoff](../../documentation/handoffs/design-context-transition-2026-10-29.md) records the final transition checks, current drawing state and first workflow trial.
