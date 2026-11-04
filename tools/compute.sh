#!/usr/bin/env bash
# Where experiments compute (issues #99, #115):
#   "aws"   each search on a throwaway AWS spot machine (c8g.8xlarge, 32 cores, tools/aws_run.py); the budget is
#           enforced: once this month's recorded AWS spend reaches it, runs go to the laptop
#   "modal" each search on Modal (CORES per run); the budget is only shown, Modal's own workspace limit stops spending
#   "local" the laptop, as before
# When the cloud cannot take a run, the laptop runs it on 4 workers. Takes effect from the next experiment; the
# loop needs no restart.
#   tools/compute.sh                                   show the setting
#   tools/compute.sh aws|modal|local [BUDGET_DOLLARS] [CORES]
set -euo pipefail
cd "$(dirname "$0")/.."
f=data/compute.json
case "${1:-}" in
  aws) printf '{"where": "aws", "budget_dollars": %s, "cpu": 32, "set": "%s"}\n' "${2:-null}" "$(date '+%Y-%m-%d %H:%M')" > "$f"; cat "$f" ;;
  modal|local) printf '{"where": "%s", "budget_dollars": %s, "cpu": %s, "set": "%s"}\n' "$1" "${2:-null}" "${3:-8}" "$(date '+%Y-%m-%d %H:%M')" > "$f"; cat "$f" ;;
  "") cat "$f" 2>/dev/null || echo '{"where": "local"} (default; no data/compute.json)' ;;
  *) echo "usage: tools/compute.sh [aws|modal|local] [BUDGET_DOLLARS] [CORES]" >&2; exit 2 ;;
esac
