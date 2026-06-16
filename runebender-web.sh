#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_PATH="${RUNEBENDER_SOURCE:-sources/VirtuaGrotesk.designspace}"
PORT="${RUNEBENDER_PORT:-8765}"
URL="http://localhost:${PORT}/"
PROFILE_DIR="${RUNEBENDER_CHROME_PROFILE:-$HOME/.runebender-web-chrome}"
CHROME_APP="${RUNEBENDER_CHROME_APP:-Google Chrome}"

cd "$ROOT_DIR"

if ! command -v runebender-serve >/dev/null 2>&1; then
  echo "runebender-serve was not found on PATH." >&2
  echo "Expected: ~/GH/repos/runebender-web/server/serve.mjs" >&2
  exit 1
fi

info_url="${URL}runebender/api/info"
expected_entry="$ROOT_DIR/$SOURCE_PATH"

open_chrome_app() {
  echo "Opening Runebender web in ${CHROME_APP} app mode:"
  echo "  url      $URL"
  echo "  profile  $PROFILE_DIR"
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
echo "  chrome  $CHROME_APP"

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
