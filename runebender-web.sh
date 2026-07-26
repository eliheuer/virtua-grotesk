#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_PATH="${RUNEBENDER_SOURCE:-sources/VirtuaGrotesk.designspace}"
PORT="${RUNEBENDER_PORT:-8765}"
URL="http://localhost:${PORT}/"
PROFILE_DIR="${RUNEBENDER_CHROME_PROFILE:-$HOME/.runebender-web-chrome}"
CHROME_APP="${RUNEBENDER_CHROME_APP:-Google Chrome}"

cd "$ROOT_DIR"

# Locate a Chromium-based browser for app mode (WebGPU). Honour an explicit
# override, otherwise probe the usual Linux/macOS binaries. Empty result on
# macOS means we fall back to `open -na "$CHROME_APP"` below.
find_browser() {
  if [[ -n "${RUNEBENDER_CHROME_BIN:-}" ]]; then
    printf '%s\n' "$RUNEBENDER_CHROME_BIN"; return 0
  fi
  local c
  for c in chromium google-chrome google-chrome-stable chromium-browser \
           brave brave-browser microsoft-edge; do
    if command -v "$c" >/dev/null 2>&1; then
      command -v "$c"; return 0
    fi
  done
  return 0
}
BROWSER_BIN="$(find_browser)"

if ! command -v runebender-serve >/dev/null 2>&1; then
  echo "runebender-serve was not found on PATH." >&2
  echo "Expected: ~/GH/repos/runebender-web/server/serve.mjs" >&2
  exit 1
fi

info_url="${URL}runebender/api/info"
expected_entry="$ROOT_DIR/$SOURCE_PATH"

open_chrome_app() {
  echo "  url      $URL"
  echo "  profile  $PROFILE_DIR"

  # Linux / explicit binary: launch the browser directly in app mode.
  # The window runs detached; a GUI launch can't be probed synchronously, so
  # we start it in the background and leave the server in the foreground.
  if [[ -n "$BROWSER_BIN" ]]; then
    echo "Opening Runebender web in $(basename "$BROWSER_BIN") app mode."
    "$BROWSER_BIN" \
      --app="$URL" \
      --new-window \
      --user-data-dir="$PROFILE_DIR" \
      --window-size=1400,900 \
      >/dev/null 2>&1 &
    disown 2>/dev/null || true
    return 0
  fi

  # macOS fallback: use `open` to launch the named Chrome app.
  if command -v open >/dev/null 2>&1; then
    echo "Opening Runebender web in ${CHROME_APP} app mode."
    if ! open -na "$CHROME_APP" --args \
      --app="$URL" \
      --new-window \
      --user-data-dir="$PROFILE_DIR"
    then
      echo "Could not open ${CHROME_APP} in app mode." >&2
      echo "Open this URL manually instead: $URL" >&2
      return 1
    fi
    if command -v osascript >/dev/null 2>&1; then
      osascript -e "tell application \"$CHROME_APP\" to activate" >/dev/null 2>&1 || true
    fi
    return 0
  fi

  echo "No Chromium-based browser found for app mode." >&2
  echo "Set RUNEBENDER_CHROME_BIN, or open this URL manually: $URL" >&2
  return 1
}

existing_info="$(curl -fsS "$info_url" 2>/dev/null || true)"
if [[ "$existing_info" == *'"server":"runebender-serve"'* ]]; then
  if [[ "$existing_info" != *"\"entryPath\":\"$expected_entry\""* ]]; then
    echo "A Runebender server is already running on ${URL}, but it is not serving:" >&2
    echo "  $expected_entry" >&2
    echo "Stop that server or set RUNEBENDER_PORT to another port." >&2
    exit 1
  fi
  echo "Using existing Runebender server at ${URL}"
  open_chrome_app
  echo "If no window appeared, check whether Chrome opened behind other windows."
  exit 0
fi

echo "Starting Runebender web:"
echo "  source  $ROOT_DIR/$SOURCE_PATH"
echo "  url     $URL"
echo "  browser ${BROWSER_BIN:-$CHROME_APP}"

runebender-serve "$SOURCE_PATH" --port "$PORT" &
server_pid=$!

cleanup() {
  if kill -0 "$server_pid" >/dev/null 2>&1; then
    kill "$server_pid" >/dev/null 2>&1 || true
    wait "$server_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

for _ in {1..50}; do
  if curl -fsS "$info_url" >/dev/null 2>&1; then
    break
  fi
  sleep 0.1
done

curl -fsS "$info_url" >/dev/null
open_chrome_app

echo "Runebender web is running. Press Ctrl+C here to stop the server."
wait "$server_pid"
