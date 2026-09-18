# Google Fonts onboarding

Official guidance checked on **2026-09-09**. This is the single active release
checklist. The [September 7 review](../archive/release-review-2026-09-07.md)
and its artifacts are historical evidence.

## Release scope

Eli confirmed **Latin, Arabic, and Hebrew** for the first release on September 9.
The family is upright, wght 400–700, with Regular, Medium, SemiBold, and Bold
instances. Italic remains a [separate proposal](../goal-google-fonts-launch.md).
Do not drop Hebrew or Arabic from the export or metadata to reduce QA findings.

The upstream is `https://github.com/eliheuer/virtua-grotesk`. Source and build
instructions are in the [README](../../README.md); the font license is
[OFL.txt](../../OFL.txt). AI assistance is disclosed in the README and article.
The public name remains **Virtua Grotesk**.

## Current evidence

[The September 9 audit](audit-2026-09-09.md) records the exact source and binary
hashes, tool versions, counts, and limitations. The sources build, but the font
is **not ready for submission acceptance**. Blank visible glyphs, interpolation,
marks, spacing, and human review remain. Automated QA is not design approval.

## Before submitting the font

- [x] Consolidate build/QA instructions and remove placeholder metadata and
  retired descriptions from the upstream root.
- [x] Use one [article draft](../article/ARTICLE.en_us.html), with no missing image
  references or unsupported model-capability claims.
- [x] Make full QA available without exclusions; make CI fail on QA failures
  and preserve diagnostic artifacts. Remove automatic tag publication.
- [x] Build and run the current Fontspector release locally.
- [ ] Resolve the drawing and engineering findings in the audit. Keep both
  masters compatible and respect protected glyph colors.
- [ ] Complete Latin, Arabic, and Hebrew shaping, mark, spacing, and weight
  review. Obtain Arabic and Hebrew reader review and Eli's drawing approval.
- [ ] Review fresh compiled-font proofs in browsers and in print. Record the
  exact binaries and source revision reviewed.
- [ ] Reproduce setup/build/QA in CI from a clean checkout. The workflow has
  been updated locally but has not yet run on GitHub.
- [ ] Confirm family-name availability, copyright/CLA identity, and that no
  restricted extended version exists. These are maintainer attestations.
- [ ] Approve final article text, specimen selection, and image licensing.
- [ ] Select a public binary delivery strategy: a reviewed release archive or
  committed release binaries. Current CI artifacts alone are not a stable
  public Packager source. Do not invent an archive URL.
- [ ] Assemble the downstream package, review metadata/subsets against actual
  support, and run full package QA with network checks enabled.
- [ ] Resolve all real FAILs and document reviewer disposition for warnings or
  exceptions. Do not silently add exclusions or suppress intended script scope.

## Starting the onboarding conversation

Google Fonts asks for an Add Font issue before a PR and asks contributors to
search for existing issues first. Its current template permits opening an issue
with requirements still unchecked and updating them later. Acceptance and
publication still require review. See the [onboarding guide](https://googlefonts.github.io/gf-guide/onboarding.html)
and [Add Font template](https://github.com/google/fonts/blob/main/.github/ISSUE_TEMPLATE/1_add-font.md).

Before posting, prepare an honest summary of scope and remaining work, one
specimen image, and the AI-use disclosure. Keep identity and license attestations
unchecked until Eli confirms them. No issue, PR, release, or public message has
been created by this cleanup.

## Downstream package

Keep downstream files separate from the upstream sources:

```text
ofl/virtuagrotesk/
  VirtuaGrotesk[wght].ttf
  METADATA.pb
  OFL.txt
  article/
    ARTICLE.en_us.html
```

The four static TTFs remain useful upstream outputs; the proposed downstream
package uses the variable font. Generate metadata from the reviewed binary with
`gftools add-font`, then review designer, category/stroke, dates, axes, subsets,
primary script, and source linkage. Keep Arabic and Hebrew in the intended
subset scope even when coverage needs work. The current local probe uses `Latn`
as a provisional primary script; confirm which script should lead the specimen.

Use [the packaging skill](../../.agents/skills/google-fonts-packaging/SKILL.md)
for a local preview. `METADATA.pb` is a downstream artifact, not a hand-written
upstream placeholder. The local probe under `out/onboarding/` is incomplete
and unpublished; its date and source metadata are not final release values.

## References

- [Upstream structure](https://googlefonts.github.io/gf-guide/upstream.html):
  source layout, public repository, build recipe, and project documentation.
- [Font requirements](https://googlefonts.github.io/gf-guide/requirements.html):
  naming, embedding, license metadata, glyphsets, and features.
- [QA](https://googlefonts.github.io/gf-guide/qa.html): Fontspector and proof review.
- [Article](https://googlefonts.github.io/gf-guide/article.html): current About
  format, replacing the retired DESCRIPTION file.
- [Metadata](https://googlefonts.github.io/gf-guide/metadata.html) and
  [packaging](https://googlefonts.github.io/gf-guide/package.html): downstream
  fields, source mappings, and package review.

Some guide pages still refer to FontBakery. Use the current QA page and the
installed Fontspector CLI for commands. Recheck the official pages at submission;
this document is not a replacement for Google Fonts review.
