#!/usr/bin/env bash
# Ask the loop to stop gracefully (issue #97): it starts no new experiment, lets the running one finish,
# records it, and then tools/run_loop.sh exits instead of starting a new session.
#   tools/stop_loop.sh            request the stop
#   tools/stop_loop.sh --cancel   take the request back
# In the loop's terminal, pressing s does the same.
set -euo pipefail
cd "$(dirname "$0")/.."
req=data/loop-stop-request
if [ "${1:-}" = "--cancel" ]; then
  rm -f "$req"; echo "Stop request cancelled; the loop carries on."
else
  date '+%Y-%m-%d %H:%M:%S' > "$req"
  echo "Stop requested. The loop will finish and record the current experiment, then stop."
fi
