#!/usr/bin/env bash
# Stop the running experiment now, with everything it started: the search, its workers and any Modal app
# (issue #104). Finished units stay in data/checkpoints/ (issue #105); starting the same attack.py again resumes
# them under the same experiment number. For a stop that lets the run finish, use tools/stop_loop.sh.
set -uo pipefail
cd "$(dirname "$0")/.."
marker=data/running-experiment.json
[ -f "$marker" ] || { echo "No experiment running."; exit 0; }
pid=$(python3 -c "import json;print(json.load(open('$marker'))['pid'])")
kill -0 "$pid" 2>/dev/null || { rm -f "$marker"; echo "No experiment running (stale marker removed)."; exit 0; }
kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid"
for _ in $(seq 1 90); do kill -0 "$pid" 2>/dev/null || break; sleep 1; done
if kill -0 "$pid" 2>/dev/null; then kill -KILL -- "-$pid" 2>/dev/null || kill -KILL "$pid"; fi
rm -f "$marker" data/experiment-progress.json
echo "Experiment stopped. Finished units are kept; start the same attack.py to resume."
