# /font-qa

Run local Google Fonts readiness checks.

## Usage

```bash
/font-qa [preflight|test|reports|proof]
```

Default: `preflight`

## Checks

### `preflight`

Run:

```bash
make preflight
```

This is the current handoff gate while drawing work is still in progress. It
builds once, regenerates reports, validates source and generated metadata, and
allows only the documented drawing/source Fontspector FAILs.

### `test`

Run:

```bash
make test
```

This builds, then runs Fontspector's `googlefonts` profile through
`scripts/check_gf_fonts.sh`. It is expected to fail until glyph coverage and
contour-count blockers are resolved or explicitly accepted by Google Fonts.

### `reports`

Run:

```bash
make reports
```

This builds, then regenerates:

- `documentation/master-compatibility.md`
- `documentation/missing-gf-latin-core.md`
- `documentation/missing-gf-arabic-core.md`
- `documentation/arabic-shaping-smoke-test.md`
- `documentation/fontspector-contour-count.md`
- `documentation/fontspector-warnings.md`
- `documentation/fontspector-googlefonts-report.md`

### `proof`

Run:

```bash
make proof
```

This builds, then regenerates `proof.pdf`.

## Notes

- Do not rely on ad hoc inline compatibility scripts when the repo-provided
  reports cover the same surface.
- Use `make reports-only` only when the current built fonts are already known
  to match the current sources.
- Review `GF_READINESS.md` and `documentation/google-fonts-upstream-audit.md`
  before claiming a handoff is ready.
