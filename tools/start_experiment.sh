#!/usr/bin/env bash
# Start the experiment in attack.py as its own process, outside any Claude Code session, so it takes as
# long as it needs (Alexis, 2026-10-27, issue #96). Arguments go to run_experiment.py (by default no
# time limit). The run is recorded in data/running-experiment.json until it ends; wait for it with
# tools/wait_experiment.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
marker=data/running-experiment.json
if [ -f "$marker" ] && kill -0 "$(python3 -c "import json;print(json.load(open('$marker'))['pid'])")" 2>/dev/null; then
  echo "An experiment is already running: $(cat "$marker")" >&2
  exit 1
fi
mkdir -p logs
log="logs/experiment-$(date +%Y%m%d-%H%M%S).log"
nohup bash -c 'uv run python run_experiment.py "$@"; echo "exit code $?"; rm -f data/running-experiment.json' \
  _ "$@" > "$log" 2>&1 < /dev/null &
pid=$!
printf '{"pid": %s, "log": "%s", "started": "%s", "args": "%s"}\n' "$pid" "$log" "$(date '+%Y-%m-%d %H:%M:%S')" "$*" > "$marker"
echo "Experiment started (pid $pid); log: $log"
