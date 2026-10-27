#!/usr/bin/env bash
# Where experiments compute (issue #99): "modal" runs each search on Modal (8 cores, paid from Alexis's Modal
# credit) and falls back to the laptop on 4 workers when Modal cannot run it; "local" runs on the laptop as before.
# Takes effect from the next experiment; the loop needs no restart.
#   tools/compute.sh            show the setting
#   tools/compute.sh modal|local [BUDGET_DOLLARS]   the budget is only shown on the dashboard; Modal's own
#                                                   workspace limit is what stops spending
set -euo pipefail
cd "$(dirname "$0")/.."
f=data/compute.json
case "${1:-}" in
  modal|local) printf '{"where": "%s", "budget_dollars": %s, "set": "%s"}\n' "$1" "${2:-null}" "$(date '+%Y-%m-%d %H:%M')" > "$f"; cat "$f" ;;
  "") cat "$f" 2>/dev/null || echo '{"where": "local"} (default; no data/compute.json)' ;;
  *) echo "usage: tools/compute.sh [modal|local]" >&2; exit 2 ;;
esac
