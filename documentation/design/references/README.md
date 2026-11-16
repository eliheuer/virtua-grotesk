# Reference roles

Virtua Grotesk is Eli's own design. The reference fonts do not dictate its
shapes, and a small difference in form from a reference font is not a defect.
A large difference is information: if a Virtua glyph is very different from
all the reference fonts, find out why before you continue.

Use the reference fonts mainly to compare these properties:

- visual weight, inside one script and between scripts;
- spacing and the texture of words;
- outline consistency, for example even stroke weight and curve quality;
- the structure that readers of the script expect.

A green Virtua source is a construction reference; read the exact GLIF and a filled
render, recording the donor master. Check its current mark color in both masters
and its component dependencies. A non-green donor is not an approved reference
even if an old note called it one.

External font families explain script structure and reading texture. The list
is `[reference_fonts.families]` in `context.md`, with the reason for
each family. `make reference-fonts` copies them into `reference-fonts/`, which
Git ignores. `make proof-web` and the proof view of Runebender read that
folder; Runebender shows the families that cover the glyph. A
supplied sketch/image records shape intent; calibrate it before using it as
dimensional evidence. Rejected candidates are counterexamples.

The canonical core set is O/H/n/o, supplemented by same-script green forms. Exact
glyph records and constructions select additional donors.

## Reference sets

| Script | Fonts |
| --- | --- |
| Arabic | Rubik, Noto Sans Arabic, IBM Plex Sans Arabic, Readex Pro |
| Hebrew | Rubik, Noto Sans Hebrew, Heebo, IBM Plex Sans Hebrew, Assistant |
| Latin accents | The shared collection of fontgarden-tools (`make accent-proofs`) |

Rubik is the quality target for weight, spacing and outline quality.
