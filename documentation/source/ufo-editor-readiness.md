# UFO Editor Readiness

This generated report checks that the active source UFOs are readable
before hand cleanup in Runebender or another UFO editor. It does not
launch the editor; it validates the on-disk UFO package with
`fontTools.ufoLib` and reads every GLIF in strict mode.

- UFO editor handoff ready: yes
- UFOs checked: 2
- GLIF read errors: 0
- Missing GLIF files: 0
- Duplicate GLIF filenames: 0

## Source UFOs

| UFO | Loadable | Layers | Glyphs | GLIF read errors | Missing files | Duplicate filenames | Ready |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `sources/VirtuaGrotesk-Regular.ufo` | yes | `public.default` | 682 | 0 | 0 | 0 | yes |
| `sources/VirtuaGrotesk-Bold.ufo` | yes | `public.default` | 682 | 0 | 0 | 0 | yes |

## Hand Cleanup Use

Run this check before opening a manual cleanup session:

```bash
make ufo-editor-check
```

If Runebender specifically failed to load the UFO, run the optional
Norad loader check against the same dependency build Runebender uses:

```bash
make runebender-ufo-check
```

Set `RUNEBENDER_REPO=/path/to/runebender-xilem` if the sibling repo
is not at `/Users/eli/GH/repos/runebender-xilem`.

If this report is not ready, fix the UFO package before drawing work.
If it is ready but an editor still fails to open the source, compare
the editor's loader error against this report and the Norad check to
separate UFO syntax problems from editor-specific loader behavior.
