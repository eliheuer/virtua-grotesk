#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT/venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
    PYTHON_BIN="$(command -v python3)"
fi

TMPDIR="$(mktemp -d "${TMPDIR:-/tmp}/virtua-designer-profile.XXXXXX")"
trap 'rm -rf "$TMPDIR"' EXIT

expect_blocked() {
    local label="$1"
    local expected="$2"
    shift 2
    local output

    if output="$("$@" 2>&1)"; then
        echo "Expected validator to block: $label"
        echo "$output"
        exit 1
    fi
    if [[ "$output" != *"$expected"* ]]; then
        echo "Expected message not found for: $label"
        echo "Expected: $expected"
        echo "$output"
        exit 1
    fi
}

write_png() {
    "$PYTHON_BIN" - "$1" "$2" "$3" <<'PY'
from __future__ import annotations

import struct
import sys
import zlib


path = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])


def chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


scanlines = b"".join(
    b"\x00" + bytes((32, 32, 32, 255)) * width
    for _ in range(height)
)
png = (
    b"\x89PNG\r\n\x1a\n"
    + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    + chunk(b"IDAT", zlib.compress(scanlines))
    + chunk(b"IEND", b"")
)
with open(path, "wb") as handle:
    handle.write(png)
PY
}

cat >"$TMPDIR/info.pb" <<'EOF'
designer: "Eli Heuer"
link: "https://eliheuer.com"
avatar {
  file_name: "eliheuer.png"
}
EOF
"$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_info.py" "$TMPDIR/info.pb" "Eli Heuer" "eliheuer.png" >/dev/null

cat >"$TMPDIR/info.pb" <<'EOF'
designer: "Wrong Name"
link: "https://eliheuer.com"
avatar {
  file_name: "eliheuer.png"
}
EOF
expect_blocked "info.pb designer spelling" 'designer should be "Eli Heuer"' \
    "$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_info.py" "$TMPDIR/info.pb" "Eli Heuer" "eliheuer.png"

cat >"$TMPDIR/info.pb" <<'EOF'
designer: "Eli Heuer"
link: "https://example.com/REPLACE-WITH-PROFILE"
avatar {
  file_name: "eliheuer.png"
}
EOF
expect_blocked "info.pb placeholder link" "not a placeholder" \
    "$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_info.py" "$TMPDIR/info.pb" "Eli Heuer" "eliheuer.png"

write_png "$TMPDIR/eliheuer.png" 120 120
"$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_image.py" "$TMPDIR/eliheuer.png" "eliheuer.png" >/dev/null

cp "$TMPDIR/eliheuer.png" "$TMPDIR/wrong.png"
expect_blocked "profile image filename" "image filename should be eliheuer.png" \
    "$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_image.py" "$TMPDIR/wrong.png" "eliheuer.png"

write_png "$TMPDIR/too-small.png" 80 80
expect_blocked "profile image minimum size" "between 100px and 300px" \
    "$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_image.py" "$TMPDIR/too-small.png" "too-small.png"

cat >"$TMPDIR/bio.html" <<'EOF'
<p>Eli Heuer is a type designer and software designer focused on open-source tools, variable fonts, and production systems for public type families. His work connects drawing, build engineering, and documentation so type projects can move from exploratory sources into durable releases. Heuer has contributed to font editors, design automation, and publishing workflows that help designers inspect sources, test generated binaries, and prepare readable handoff materials.</p>

<p><a href="https://eliheuer.com" target="_blank">eliheuer.com</a></p>
EOF
"$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_bio.py" "$TMPDIR/bio.html" >/dev/null

cat >"$TMPDIR/bio.html" <<'EOF'
<p>Eli Heuer is a type designer and software designer focused on open-source tools, variable fonts, and production systems for public type families. His work connects drawing, build engineering, and documentation so type projects can move from exploratory sources into durable releases. Heuer has contributed to font editors, design automation, and publishing workflows that help designers inspect sources, test generated binaries, and prepare readable handoff materials.</p>

<p><a href="https://REPLACE-WITH-APPROVED-URL" target="_blank">REPLACE-WITH-APPROVED-LABEL</a></p>
EOF
expect_blocked "bio placeholder URL" "should not use a placeholder URL" \
    "$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_bio.py" "$TMPDIR/bio.html"

cat >"$TMPDIR/bio.html" <<'EOF'
<p>I am a type designer and software designer focused on open-source tools, variable fonts, and production systems for public type families. My work connects drawing, build engineering, and documentation so type projects can move from exploratory sources into durable releases. Heuer has contributed to font editors, design automation, and publishing workflows that help designers inspect sources, test generated binaries, and prepare readable handoff materials.</p>

<p><a href="https://eliheuer.com" target="_blank">eliheuer.com</a></p>
EOF
expect_blocked "bio first-person voice" "third person, not first person" \
    "$PYTHON_BIN" "$ROOT/scripts/validate_designer_profile_bio.py" "$TMPDIR/bio.html"

PROFILE_GF_REPO="$TMPDIR/fonts"
PROFILE_INPUTS="$TMPDIR/profile-inputs"
mkdir -p "$PROFILE_INPUTS"
git init -q "$PROFILE_GF_REPO"
git -C "$PROFILE_GF_REPO" -c user.name="Eli Heuer" -c user.email="eli@example.com" commit --allow-empty -m "Initial test checkout" >/dev/null
mkdir -p "$PROFILE_GF_REPO/catalog/designers"

cat >"$PROFILE_INPUTS/info.pb" <<'EOF'
designer: "Eli Heuer"
link: "https://eliheuer.com"
avatar {
  file_name: "eliheuer.png"
}
EOF

cat >"$PROFILE_INPUTS/bio.html" <<'EOF'
<p>Eli Heuer is a type designer and software designer focused on open-source tools, variable fonts, and production systems for public type families. His work connects drawing, build engineering, and documentation so type projects can move from exploratory sources into durable releases. Heuer has contributed to font editors, design automation, and publishing workflows that help designers inspect sources, test generated binaries, and prepare readable handoff materials.</p>

<p><a href="https://eliheuer.com" target="_blank">eliheuer.com</a></p>
EOF

write_png "$PROFILE_INPUTS/eliheuer.png" 120 120

"$PYTHON_BIN" "$ROOT/scripts/prepare_designer_profile.py" \
    --info "$PROFILE_INPUTS/info.pb" \
    --bio "$PROFILE_INPUTS/bio.html" \
    --image "$PROFILE_INPUTS/eliheuer.png" \
    --gf-repo "$PROFILE_GF_REPO" >/tmp/virtua-profile-prepare.out

if [[ -e "$PROFILE_GF_REPO/catalog/designers/eliheuer/info.pb" ]]; then
    echo "prepare helper wrote files during dry run"
    cat /tmp/virtua-profile-prepare.out
    exit 1
fi
if ! grep -q "Ready to apply: yes" /tmp/virtua-profile-prepare.out; then
    echo "prepare helper did not report ready for valid inputs"
    cat /tmp/virtua-profile-prepare.out
    exit 1
fi

cat >"$PROFILE_INPUTS/info.pb" <<'EOF'
designer: "Eli Heuer"
link: "https://github.com/eliheuer"
avatar {
  file_name: "eliheuer.png"
}
EOF

expect_blocked "profile prepare link mismatch" "info.pb link should match one bio.html link" \
    "$PYTHON_BIN" "$ROOT/scripts/prepare_designer_profile.py" \
    --info "$PROFILE_INPUTS/info.pb" \
    --bio "$PROFILE_INPUTS/bio.html" \
    --image "$PROFILE_INPUTS/eliheuer.png" \
    --gf-repo "$PROFILE_GF_REPO" \
    --apply

cat >"$PROFILE_INPUTS/info.pb" <<'EOF'
designer: "Eli Heuer"
link: ""
avatar {
  file_name: "eliheuer.png"
}
EOF

"$PYTHON_BIN" "$ROOT/scripts/prepare_designer_profile.py" \
    --info "$PROFILE_INPUTS/info.pb" \
    --bio "$PROFILE_INPUTS/bio.html" \
    --image "$PROFILE_INPUTS/eliheuer.png" \
    --gf-repo "$PROFILE_GF_REPO" >/tmp/virtua-profile-prepare-blank-link.out

if ! grep -q "Ready to apply: yes" /tmp/virtua-profile-prepare-blank-link.out; then
    echo "prepare helper should allow a blank info.pb link when bio links validate"
    cat /tmp/virtua-profile-prepare-blank-link.out
    exit 1
fi

cat >"$PROFILE_INPUTS/info.pb" <<'EOF'
designer: "Eli Heuer"
link: "https://eliheuer.com"
avatar {
  file_name: "eliheuer.png"
}
EOF

"$PYTHON_BIN" "$ROOT/scripts/prepare_designer_profile.py" \
    --info "$PROFILE_INPUTS/info.pb" \
    --bio "$PROFILE_INPUTS/bio.html" \
    --image "$PROFILE_INPUTS/eliheuer.png" \
    --gf-repo "$PROFILE_GF_REPO" \
    --apply >/dev/null

for path in \
    "$PROFILE_GF_REPO/catalog/designers/eliheuer/info.pb" \
    "$PROFILE_GF_REPO/catalog/designers/eliheuer/bio.html" \
    "$PROFILE_GF_REPO/catalog/designers/eliheuer/eliheuer.png"
do
    if [[ ! -f "$path" ]]; then
        echo "prepare helper did not write expected file: $path"
        exit 1
    fi
done

expect_blocked "profile prepare existing target" "target designer profile already exists" \
    "$PYTHON_BIN" "$ROOT/scripts/prepare_designer_profile.py" \
    --info "$PROFILE_INPUTS/info.pb" \
    --bio "$PROFILE_INPUTS/bio.html" \
    --image "$PROFILE_INPUTS/eliheuer.png" \
    --gf-repo "$PROFILE_GF_REPO" \
    --apply

DIRTY_GF_REPO="$TMPDIR/fonts-dirty"
git init -q "$DIRTY_GF_REPO"
git -C "$DIRTY_GF_REPO" -c user.name="Eli Heuer" -c user.email="eli@example.com" commit --allow-empty -m "Initial test checkout" >/dev/null
mkdir -p "$DIRTY_GF_REPO/catalog/designers"
printf 'dirty\n' >"$DIRTY_GF_REPO/README.md"
expect_blocked "profile prepare dirty checkout" "dirty paths outside the designer profile path: README.md" \
    "$PYTHON_BIN" "$ROOT/scripts/prepare_designer_profile.py" \
    --info "$PROFILE_INPUTS/info.pb" \
    --bio "$PROFILE_INPUTS/bio.html" \
    --image "$PROFILE_INPUTS/eliheuer.png" \
    --gf-repo "$DIRTY_GF_REPO" \
    --apply

expect_blocked "profile prepare missing image" "image file does not exist" \
    "$PYTHON_BIN" "$ROOT/scripts/prepare_designer_profile.py" \
    --info "$PROFILE_INPUTS/info.pb" \
    --bio "$PROFILE_INPUTS/bio.html" \
    --image "$PROFILE_INPUTS/missing.png" \
    --gf-repo "$PROFILE_GF_REPO" \
    --replace \
    --apply

echo "Designer profile validator tests passed."
