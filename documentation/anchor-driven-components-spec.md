# Anchor-driven components — research spec (parked)

Researched 2026-08-12, then parked to focus on shipping the font. This is
everything needed to pick the feature up later; no code was written.

**The feature:** moving a base glyph's anchor moves every mark component
attached to it, with lock/unlock and enable/disable-alignment, matching
Glyphs. Target: Runebender (`~/GH/repos/runebender-web`), so that people
without a Mac can do this work.

## Why it is worth building

No open-source or browser-based editor does live anchor-driven component
placement today. Glyphs and FontLab are the only shipping implementations.
Fontra wants it and has not built it — Just van Rossum on
[fontra#2700](https://github.com/fontra/fontra/issues/2700):

> "Something like this will indeed come to Fontra. Additionally, I would
> like composition with anchors to be **responsive**, so that editing
> anchors will be reflected in the diacritics. This functionality has
> quite a high priority, yet I cannot give you a concrete timeline."

FontForge and RoboFont are one-shot (regenerate the composite); Birdfont
has no anchor system at all. Runebender would be first in the browser.

Google Fonts already treats it as the correct authoring state
([gf-guide diacritics](https://googlefonts.github.io/gf-guide/diacritics.html)):

> "ideally, automatic alignment should be enabled consistently in the
> composite glyphs. This way they would get automatically updated after
> any change on any of the components is performed."

## Behaviour to copy from Glyphs

**The governing rule.** Auto-alignment is ON by default when a layer
contains ONLY components, and switches off the moment any real path is
added — anchors are then ignored entirely. (In this repo `teh-ar.init` is
exactly that case: a drawn tooth plus a dot component, so Glyphs would not
auto-align it either.)

**State is three-valued, per component**, from `GSComponent`:

| value | meaning |
|---|---|
| `alignment = -1` | disabled |
| `alignment = 0` | default (auto) |
| `alignment = 1` | forced |

plus an optional `anchor` name to disambiguate when more than one
`anchor`/`_anchor` pair would match (`top`, `top_alt`, `top_viet` …),
chosen from an anchor picker in the component info box.

**Two separate context-menu concepts** — do not merge them:

- *Disable / Enable Automatic Alignment* — breaks the link, component
  becomes freely draggable.
- *Lock / Unlock Component* — cannot be moved, but keeps its alignment.
  In Glyphs 4 locking is at SHAPE level ("do not move locked shapes"), so
  paths lock too — one mechanism, not two.

Glyphs 4 also adds *Enable Automatic Alignment in all Masters*, and a
font-wide switch in Font Info > Other.

**Colour is the state indicator**, not an icon:

| state | colour |
|---|---|
| plain component | grey |
| auto-aligned component | green |
| number-category component | blue |

Anchors: underscore anchors are drawn **hollow**.

**Anchor conventions** (already what this repo's sources do):

- Bases carry `top`, `bottom`, `center`, `ogonek`; marks carry `_top`,
  `_bottom` …
- A mark carrying BOTH `_top` and `top` is what generates `mkmk`.
- Attachment walks backwards: a mark's `_top` connects to the matching
  anchor in the nearest preceding glyph, falling back through earlier
  marks to the base letter.
- Composites prefer `.case` mark variants over capitals.
- Mark components positioned by anchors do NOT affect the composite's
  sidebearings; the aligned component drives them.

**Commands worth having:** `Set Anchors` (Cmd-U) and `Reset Anchors`
(Cmd-Opt-U) add/redo default anchors on a selection — this repo currently
does that offline in `scripts/arabic_anchors.py` and
`scripts/latin_marks.py`. Also `Make Component Glyph` (Cmd-Opt-Shift-C).

**Mark cloud:** selecting an anchor shows a grey preview of every mark
that could attach there. Toggleable in Appearance settings.

**Glyphs 4 extras:** `_top@centerX` anchor-to-metric annotations applied
across glyphs; `*origin` anchor participates in aligned-component export;
`GSAlignmentHorizontal` manually settable as an escape hatch.

## How to persist it in a UFO — the important part

The UFO spec has **no** native way to record that a component is
anchor-attached. `<component>` allows only `base`, the four scale/skew
attributes, `xOffset`, `yOffset`, `identifier`.

**Use `public.objectLibs`.** UFO3 defines this glyph-lib key as a
dictionary of object identifiers to per-object dicts, explicitly covering
components and anchors. Store, keyed by the component's `identifier`:

```
"org.runebender.componentAlignment": {"mode": "auto"|"off"|"forced",
                                      "anchor": "top"}
```

Why this and not the Glyphs key: **glyphsLib's
`com.schriftgestaltung.Glyphs.ComponentInfo` is keyed by LIST INDEX**, and
their own source carries `# FIXME: (jany) move to using component
identifiers for robustness`. Reorder or insert a component in another
editor and the alignment silently detaches. `public.objectLibs` is
identifier-keyed and does not have that failure mode.

Support:

- **norad** (Rust — Runebender's own backend): full support.
  `Component { base, transform, identifier, lib }`, plus
  `load_object_libs()` / `dump_object_libs()`. norad *manages* the key and
  errors if you set it manually.
- **ufoLib2** (what fontmake uses): full support, auto-assigns a UUID4
  identifier, prunes stale entries on save.
- **defcon / RoboFont**: no objectLibs handling — preserves the data
  opaquely but never prunes, so tolerate orphaned identifiers on read.
- **fontmake / gftools**: lib data never reaches the binary, so this is
  inert at build time. Safe.

For Glyphs interop, **mirror** the same state into
`com.schriftgestaltung.Glyphs.ComponentInfo` on write and read it as a
fallback on import. Note `ufo2glyphs` DISABLES automatic alignment by
default — `--enable-automatic-alignment` is needed to keep it — but a
UFO composite with no ComponentInfo imports with `alignment = 0`, i.e.
auto ON.

**Repo constraint:** per CLAUDE.md these UFOs must never be saved through
defcon/ufoLib `font.save()`. Both the lib entry and the `identifier`
attribute have to be written in the repo's native glif style by hand, and
`identifier` should only be emitted on components that actually carry
alignment state (norad's docs advise the same).

## UX to borrow from elsewhere

- **FontLab** proves live cross-composite update is practical: with the
  Auto layer property, moving an anchor in a component glyph moves the
  accent in every composite using it. It also has an explicit per-element
  *Anchored* property.
- **FontForge's Anchor Control** panel (`Metrics > Anchor Control`) shows
  one anchor class at a time with every base tiled against every mark —
  the right model for reviewing a whole anchor class at once.
- **Fontra** decomposes component transforms (translate/rotate/scale/skew
  plus a transformation centre) rather than storing a raw matrix. Worth
  copying independently of this feature.
- **RoboFont's AnchorOverlayTool** shows all accents live on the base
  while dragging the anchor — the mark cloud, essentially.

## Where this repo already fits

The font data is already in the shape the feature needs. Every Arabic mark
carries a `_`-anchor, every base carries its slots, and `top`/`bottom` are
separated from `topDots`/`bottomDots` (Rubik's split). The editor work is
to recompute `base.slot − mark._slot` on anchor drag and offer a detach
that falls back to a stored freeform offset.

Until then, `make arabic-sync` does the same job offline.

## Sources

[Glyphs handbook: Components](https://handbook.glyphsapp.com/components/) ·
[Anchors](https://handbook.glyphsapp.com/anchors/) ·
[Mark attachment](https://glyphsapp.com/learn/mark-attachment) ·
[Glyphs 4.0 changelog](https://updates.glyphsapp.com/Glyphs4.0-4000.html) ·
[UFO3 GLIF spec](https://unifiedfontobject.org/versions/ufo3/glyphs/glif/) ·
[glyphsLib](https://github.com/googlefonts/glyphsLib) ·
[GlyphsSDK](https://github.com/schriftgestalt/GlyphsSDK) ·
[fontra#2700](https://github.com/fontra/fontra/issues/2700) ·
[Fontra shaping blog](https://blog.fontra.xyz/blog/opentype-harfbuzz/) ·
[fontra-glyphs](https://github.com/googlefonts/fontra-glyphs) ·
[gf-guide diacritics](https://googlefonts.github.io/gf-guide/diacritics.html) ·
[FontLab Composite and Auto Glyphs](https://help.fontlab.com/fontlab/7/manual/Composite-and-Auto-Glyphs/) ·
[FontForge Anchor Control](https://fontforge.org/docs/ui/dialogs/anchorcontrol.html) ·
[AnchorOverlayTool](https://github.com/jenskutilek/AnchorOverlayTool)
