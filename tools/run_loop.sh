#!/usr/bin/env bash
# Start the autoresearch loop as its own Claude Code session, in this repository.
#
#   tools/run_loop.sh                       interactive: you see it work and approve its commands
#   tools/run_loop.sh --unattended          headless, no permission prompts; progress on screen, full log in logs/
#   uv run python tools/loop_watch.py --follow logs/loop-...log   watch a running loop from another shell
#
# There are no milestones (Alexis, 2026-10-27, issue #92). Headless, the loop works every open item in
# order-of-work.md and starts a new session whenever one ends, until data/loop-stop.json says why to stop:
# a reading passed every gate (a possible solution, for Alexis to check) or nothing is left open. Delete that
# file to start again after reviewing it. Five sessions in a row that end within five minutes also stop it.
#
# The prompt is tools/loop_prompt.md; edit it to change what the loop does. Its transcript is synced into
# transcripts/ by the hooks in .claude/settings.json like any other session.
set -euo pipefail
cd "$(dirname "$0")/.."

mode=interactive
while [ $# -gt 0 ]; do
  case "$1" in
    --unattended) mode=unattended; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

stop=data/loop-stop.json
if [ -f "$stop" ]; then
  echo "The loop stopped earlier: $(cat "$stop")"
  echo "Review it, then delete $stop to start again."
  exit 1
fi

prompt="$(cat tools/loop_prompt.md)"

if [ "$mode" = interactive ]; then
  git pull -q --rebase --autostash || true
  exec claude "$prompt"
fi

mkdir -p logs
quick=0
while [ ! -f "$stop" ]; do
  git pull -q --rebase --autostash || true
  log="logs/loop-$(date +%Y%m%d-%H%M%S).log"
  echo "Loop session starting; log: $log"
  t0=$(date +%s)
  claude -p "$prompt" --dangerously-skip-permissions --output-format stream-json --verbose 2>&1 \
    | tee "$log" | uv run python -u tools/loop_watch.py || true
  echo "Loop session ended; full log: $log"
  # the record commits that followed the last experiment go public too (tools/publish.py)
  uv run python tools/publish.py >> logs/publish.log 2>&1 || echo "publish failed; see logs/publish.log"
  if [ $(( $(date +%s) - t0 )) -lt 300 ]; then quick=$((quick + 1)); else quick=0; fi
  if [ "$quick" -ge 5 ]; then
    echo "Five sessions in a row ended within five minutes; stopping. See the last logs in logs/."
    exit 1
  fi
  [ -f "$stop" ] || sleep 30
done
echo "Loop stopped: $(cat "$stop")"
