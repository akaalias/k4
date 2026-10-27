#!/usr/bin/env bash
# Wait for the experiment started by tools/start_experiment.sh, at most MAX seconds per call (default 540,
# under a tool call's 10-minute limit), then report. Call it again until it says the run has ended.
# Exit 0: no run in progress (finished, or none started). Exit 3: still running.
set -uo pipefail
cd "$(dirname "$0")/.."
marker=data/running-experiment.json
max=${1:-540}
t=0
while [ -f "$marker" ] && [ "$t" -lt "$max" ]; do
  pid=$(python3 -c "import json;print(json.load(open('$marker'))['pid'])" 2>/dev/null || echo 0)
  kill -0 "$pid" 2>/dev/null || { rm -f "$marker"; break; }
  sleep 15; t=$((t + 15))
done
if [ -f "$marker" ]; then
  log=$(python3 -c "import json;print(json.load(open('$marker'))['log'])")
  echo "Still running: $(cat "$marker")"
  echo "Last lines of $log:"; tail -n 5 "$log"
  exit 3
fi
last=$(ls -t logs/experiment-*.log 2>/dev/null | head -1)
echo "No experiment running."
[ -n "$last" ] && { echo "Last lines of $last:"; tail -n 5 "$last"; }
exit 0
