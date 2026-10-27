#!/usr/bin/env bash
# Start the autoresearch loop as its own Claude Code session, in this repository.
#
#   tools/run_loop.sh                       interactive: you see it work and approve its commands
#   tools/run_loop.sh --unattended          headless, no permission prompts: the loop runs in the background and this
#                                           terminal shows its dashboard (q closes it; tools/loop_tui.sh reopens it)
#   uv run python tools/loop_watch.py --follow logs/loop-...log   watch a running loop from another shell
#
# There are no milestones (Alexis, 2026-10-27, issue #92). Headless, the loop works every open item in
# order-of-work.md and starts a new session whenever one ends, until data/loop-stop.json says why to stop:
# a reading passed every gate (a possible solution, for Alexis to check) or nothing is left open. Delete that
# file to start again after reviewing it. Five sessions in a row that end within five minutes also stop it.
# To stop it gracefully, press s in the dashboard (s again takes it back) or run tools/stop_loop.sh: it starts
# no new experiment, finishes and records the current one, and exits.
#
# The prompt is tools/loop_prompt.md; edit it to change what the loop does. Its transcript is synced into
# transcripts/ by the hooks in .claude/settings.json like any other session.
set -euo pipefail
cd "$(dirname "$0")/.."

mode=interactive
while [ $# -gt 0 ]; do
  case "$1" in
    --unattended) mode=unattended; shift ;;
    --service) mode=service; shift ;;          # internal: the loop itself, started in the background
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

# --unattended (issue #98): the loop runs as a background service that survives closing this terminal,
# and this terminal shows the dashboard. q closes the dashboard; tools/loop_tui.sh reopens it anywhere.
pidf=data/loop.pid
if [ "$mode" = unattended ]; then
  if [ -f "$pidf" ] && kill -0 "$(cat "$pidf")" 2>/dev/null; then
    echo "The loop is already running (pid $(cat "$pidf")); opening the dashboard."
  else
    mkdir -p logs
    nohup "$0" --service >> logs/runner.log 2>&1 < /dev/null &
    echo "Loop started in the background (pid $!); its own log: logs/runner.log"
    sleep 1
  fi
  if [ -t 1 ]; then exec tools/loop_tui.sh; fi
  exit 0
fi

echo $$ > "$pidf"
trap 'rm -f "$pidf"' EXIT
mkdir -p logs
quick=0
req=data/loop-stop-request          # a graceful stop: press s in the dashboard, or tools/stop_loop.sh (issue #97)
rm -f "$req"
while [ ! -f "$stop" ] && [ ! -f "$req" ]; do
  git pull -q --rebase --autostash || true
  log="logs/loop-$(date +%Y%m%d-%H%M%S).log"
  echo "Loop session starting; log: $log"
  t0=$(date +%s)
  claude -p "$prompt" --dangerously-skip-permissions --output-format stream-json --verbose > "$log" 2>&1 || true
  echo "Loop session ended; full log: $log"
  # the record commits that followed the last experiment go public too (tools/publish.py)
  uv run python tools/publish.py >> logs/publish.log 2>&1 || echo "publish failed; see logs/publish.log"
  if [ $(( $(date +%s) - t0 )) -lt 300 ]; then quick=$((quick + 1)); else quick=0; fi
  if [ "$quick" -ge 5 ]; then
    echo "Five sessions in a row ended within five minutes; stopping. See the last logs in logs/."
    exit 1
  fi
  [ -f "$stop" ] || [ -f "$req" ] || sleep 30
done
if [ -f "$req" ]; then
  rm -f "$req"
  if [ -f data/running-experiment.json ]; then
    echo "Loop stopped at your request. An experiment is still running on its own: $(cat data/running-experiment.json)"
    echo "Its record is written when it ends; the next loop session will read it."
  else
    echo "Loop stopped at your request, after recording the last experiment."
  fi
  exit 0
fi
echo "Loop stopped: $(cat "$stop")"
