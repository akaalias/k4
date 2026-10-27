#!/usr/bin/env bash
# Open the loop's dashboard (issue #98). q closes it; the loop keeps running.
cd "$(dirname "$0")/.." && exec uv run --quiet --with rich python tools/loop_tui.py
