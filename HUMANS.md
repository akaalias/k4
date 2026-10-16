# For humans: how to run this project

The agent reads `program.md`; this page is for you.

**The site.** Start the dashboard and open http://127.0.0.1:8765:

```
uv run python dashboard.py
```

Use `uv run`, not plain `python3`; without it the markdown pages show raw text.

**The loop.** Start the autoresearch loop as its own Claude Code session, in a separate terminal, while
you keep working on anything else:

```
tools/run_loop.sh                    # interactive: you watch it work and approve its commands
tools/run_loop.sh --unattended       # runs on its own with no permission prompts; log in logs/
tools/run_loop.sh --stop-after F8    # stop once that family is closed or blocked (default F6)
```

It follows `program.md` and works the open items in `order-of-work.md` (the Priorities page) from the top.
What it is told to do is in `tools/loop_prompt.md`; edit that file to change it. `--unattended` switches off
every permission check, so only use it when you are happy for it to run commands without asking.

**One experiment by hand.**

```
uv run --with pytest pytest -q      # the ruler must match K1-K3 before any run
uv run python run_experiment.py     # runs attack.py once, writes the record, commits it
```

**Transcripts.** Every chat and agent log is mirrored into `transcripts/` and pushed by the hooks in
`.claude/settings.json` (after each turn, before compaction, at session end). To sync by hand:

```
uv run python tools/sync_transcripts.py --commit
```
