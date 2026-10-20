#!/usr/bin/env bash
# Start the autoresearch loop as its own Claude Code session, in this repository.
#
#   tools/run_loop.sh                       interactive: you see it work and approve its commands
#   tools/run_loop.sh --unattended          headless, no permission prompts; progress on screen, full log in logs/
#   uv run python tools/loop_watch.py --follow logs/loop-...log   watch a running loop from another shell
#   tools/run_loop.sh --stop-after A1       stop once stage 2 step 2's slip table has no open row (the default since
#                                           2026-10-20; A3 was the control table; a family name such as F6 stops once
#                                           that family is closed or blocked)
#
# The prompt is tools/loop_prompt.md; edit it to change what the loop does. Its transcript is synced into
# transcripts/ by the hooks in .claude/settings.json like any other session.
set -euo pipefail
cd "$(dirname "$0")/.."

mode=interactive
stop_after=A1
while [ $# -gt 0 ]; do
  case "$1" in
    --unattended) mode=unattended; shift ;;
    --stop-after) stop_after="$2"; shift 2 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

prompt="$(cat tools/loop_prompt.md)

STOP_AFTER: $stop_after."

git pull -q --rebase --autostash || true

if [ "$mode" = unattended ]; then
  mkdir -p logs
  log="logs/loop-$(date +%Y%m%d-%H%M%S).log"
  echo "Loop running headless until $stop_after; log: $log"
  claude -p "$prompt" --dangerously-skip-permissions --output-format stream-json --verbose 2>&1 \
    | tee "$log" | uv run python -u tools/loop_watch.py
  echo "Loop finished; full log: $log"
  # the record commits that followed the last experiment go public too (tools/publish.py)
  uv run python tools/publish.py >> logs/publish.log 2>&1 || echo "publish failed; see logs/publish.log"
else
  exec claude "$prompt"
fi
