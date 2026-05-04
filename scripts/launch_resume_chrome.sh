#!/bin/zsh
set -euo pipefail

# Launch an isolated Google Chrome instance for the resume workspace.
#
# Why this exists:
# - avoid sharing a browser/profile with Playwright or daily browsing
# - keep a stable remote-debugging target for Codex
# - mirror DevToolsActivePort into the path the Chrome DevTools MCP expects
#
# Defaults can be overridden via environment variables:
#   RESUME_CHROME_PORT=9224
#   RESUME_CHROME_PROFILE=/tmp/codex-resume-chrome
#   RESUME_CHROME_URL=https://www.linkedin.com/jobs

CHROME_APP="/Applications/Google Chrome.app"
CHROME_BIN="$CHROME_APP/Contents/MacOS/Google Chrome"

PORT="${RESUME_CHROME_PORT:-9224}"
PROFILE_DIR="${RESUME_CHROME_PROFILE:-/tmp/codex-resume-chrome}"
START_URL="${RESUME_CHROME_URL:-about:blank}"
DEFAULT_PROFILE_DIR="$PROFILE_DIR/Default"
DISABLED_FEATURES="ChromeWhatsNewUI,SigninInterception,SignInProfileCreationInterception,SignInPromo,IdentityDiscAccountMenu,AccountConsistency,EnableSyncConsent"

# The DevTools MCP in this environment looks here for the active port file.
MCP_PORT_FILE="$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"
PROFILE_PORT_FILE="$PROFILE_DIR/DevToolsActivePort"

usage() {
  cat <<EOF
Usage: $(basename "$0") [--status] [--print-port-file] [url]

Launches a dedicated Chrome instance for the resume workspace using:
  port:        $PORT
  profile dir: $PROFILE_DIR

Options:
  --status           Show whether the configured port is listening and whether
                     the profile/default port files exist.
  --print-port-file  Print the mirrored DevToolsActivePort file path.

Environment overrides:
  RESUME_CHROME_PORT
  RESUME_CHROME_PROFILE
  RESUME_CHROME_URL
EOF
}

status() {
  echo "port=$PORT"
  echo "profile_dir=$PROFILE_DIR"
  echo "profile_port_file=$PROFILE_PORT_FILE"
  echo "mcp_port_file=$MCP_PORT_FILE"
  echo
  if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "listener=up"
  else
    echo "listener=down"
  fi
  if [[ -f "$PROFILE_PORT_FILE" ]]; then
    echo "profile_port_file_exists=yes"
    echo "profile_port_file_contents:"
    cat "$PROFILE_PORT_FILE"
  else
    echo "profile_port_file_exists=no"
  fi
  echo
  if [[ -L "$MCP_PORT_FILE" || -f "$MCP_PORT_FILE" ]]; then
    echo "mcp_port_file_exists=yes"
    echo "mcp_port_file_contents:"
    cat "$MCP_PORT_FILE"
  else
    echo "mcp_port_file_exists=no"
  fi
}

ensure_requirements() {
  if [[ ! -x "$CHROME_BIN" ]]; then
    echo "Google Chrome binary not found at: $CHROME_BIN" >&2
    exit 1
  fi

  mkdir -p "$PROFILE_DIR"
  mkdir -p "$DEFAULT_PROFILE_DIR"
  mkdir -p "$(dirname "$MCP_PORT_FILE")"
}

seed_profile_preferences() {
  python3 - "$PROFILE_DIR" "$DEFAULT_PROFILE_DIR" <<'PY'
import json
import sys
from pathlib import Path

profile_dir = Path(sys.argv[1])
default_profile_dir = Path(sys.argv[2])


def load_json(path):
    if not path.exists() or path.stat().st_size == 0:
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def save_json(path, data):
    path.write_text(json.dumps(data, separators=(",", ":"), sort_keys=True))


local_state_path = profile_dir / "Local State"
local_state = load_json(local_state_path)
local_state.setdefault("browser", {})["has_seen_welcome_page"] = True
local_state.setdefault("distribution", {}).update(
    {
        "import_bookmarks": False,
        "import_history": False,
        "import_home_page": False,
        "import_search_engine": False,
        "make_chrome_default_for_user": False,
        "show_welcome_page": False,
        "skip_first_run_ui": True,
        "suppress_first_run_default_browser_prompt": True,
    }
)
save_json(local_state_path, local_state)

preferences_path = default_profile_dir / "Preferences"
preferences = load_json(preferences_path)
preferences.setdefault("signin", {})["allowed"] = False
preferences.setdefault("sync", {})["feature_status_for_sync_to_signin"] = 5
preferences.setdefault("browser", {})["check_default_browser"] = False
save_json(preferences_path, preferences)
PY
}

launch() {
  if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Chrome debugging port $PORT is already listening."
  else
    seed_profile_preferences
    open -na "$CHROME_APP" --args \
      --no-first-run \
      --no-default-browser-check \
      --disable-default-apps \
      --disable-sync \
      --disable-signin-promos \
      --disable-features="$DISABLED_FEATURES" \
      --remote-debugging-port="$PORT" \
      --user-data-dir="$PROFILE_DIR" \
      "$START_URL"
  fi
}

mirror_port_file() {
  local waited=0
  local version_json ws_path

  while ! version_json="$(curl -fsS "http://127.0.0.1:$PORT/json/version" 2>/dev/null)" && [[ $waited -lt 50 ]]; do
    sleep 0.2
    waited=$((waited + 1))
  done

  if [[ -z "${version_json:-}" ]]; then
    echo "Timed out waiting for Chrome to answer http://127.0.0.1:$PORT/json/version" >&2
    exit 1
  fi

  ws_path="$(printf '%s\n' "$version_json" | sed -n 's/.*"webSocketDebuggerUrl": "ws:\/\/127\.0\.0\.1:'"$PORT"'\([^"]*\)".*/\1/p')"
  if [[ -z "$ws_path" ]]; then
    echo "Chrome responded on port $PORT, but webSocketDebuggerUrl was not found in /json/version" >&2
    exit 1
  fi

  printf "%s\n%s\n" "$PORT" "$ws_path" > "$PROFILE_PORT_FILE"
  python3 - "$PROFILE_PORT_FILE" "$MCP_PORT_FILE" <<'PY'
import sys
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])

if target.is_symlink() or target.exists():
    target.unlink()
target.write_text(source.read_text())
PY
}

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  --status)
    ensure_requirements
    status
    exit 0
    ;;
  --print-port-file)
    echo "$MCP_PORT_FILE"
    exit 0
    ;;
esac

if [[ $# -gt 0 ]]; then
  START_URL="$1"
fi

ensure_requirements
launch
mirror_port_file

echo "Resume Chrome launched."
echo "port=$PORT"
echo "profile_dir=$PROFILE_DIR"
echo "mcp_port_file=$MCP_PORT_FILE"
