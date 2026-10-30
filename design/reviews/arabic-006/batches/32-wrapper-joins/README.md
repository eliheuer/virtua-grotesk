# Non-green wrapper joining widths

Nineteen source files change only their advance width to match the existing
untransformed joining base. No outlines, component placements, anchors, colors,
features or donors change. Names and exact old/new advances are in candidate.json.
The largest core correction is Regular final Jeem,960to704; initial Ghain, Khah,
Noon, Qaf, Feh, Sheen and Theh also had stale metrics. Other selected composites
include hamza-bearing Yeh/Waw and Bold Alef variants. Green Jeem initial/medial
and all Beh/Heh reserved files remain untouched, including their mismatches.

Each wrapper has exactly two components, an untransformed joining base, no local
contours and no component consumers. Source hash guards cover all active files.
Compiled verification at400/550/700 checks every glyph's decomposed ink is exactly
unchanged and that only listed advances differ. Shaping checks preserve names,
clusters and offsets, with only intended advance changes. Human grades remain.

This repairs join spacing, not the underlying script forms. Protected Regular
Jeem initial/medial overlap and reserved Beh initial width mismatch remain visible.
Maksura/Yeh structure and Heh/Goal/Kaf/Lam-Alef design issues remain on the human
or protected repair list; matching wrapper widths does not approve those drawings.

Applied after scratch preflight and whole-row image inspection: group1 at400/550/700,
groups2/3 at400 and composite pairs at700. The disconnected Regular final Jeem
now joins; selected initial joins no longer have stale-width overlaps/gaps.
The images also retain visibly inadequate Yeh returns, cramped Theh dot groups
and Alef-below-hamza collision with Beh dots. These are separate drawing/placement
issues, not fixed by this metrics batch. No visual approval is claimed.
All compiled ink at400/550/700 is unchanged;30 shaping comparisons pass.
