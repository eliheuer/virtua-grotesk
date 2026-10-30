# Learning from design work

The grid makes consistent source geometry usable as learning data. Preserve exact
source edits and human verdicts; renderings alone lose editable structure.

Correction records in `../corrections/records/` identify draft, correction, source
hashes, topology relationship, human feedback, application and review states.
Keep point-delta pairs, structural edits and rejected examples distinct. A human
edit is not automatically a positive training pair; explicit approval and corpus
curation are separate. Preserve contour alignment decisions and raw source bytes.

Do not infer a pair solely from an orange/purple-to-green color transition. The
companion font-garden-lab extractor still uses a legacy orange-ancestor convention;
it has not been changed by this repository migration. Exporters must use these
explicit records before making training-quality claims.

Freeze parent identities before interpolation or augmentation; keep related
construction families and derived weights in one evaluation split. Measure held-out
quality and human correction effort. Automation of optical proposals requires
separate evidence; green remains a human grade.
