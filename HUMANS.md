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
tools/run_loop.sh --stop-after F8    # stop once that family is closed or blocked (default F9, the last)
```

With `--unattended` the terminal shows one line per step: the phase, the experiment being written, each finished experiment with its decision, and the elapsed time; the full stream goes to `logs/`. To watch a running loop from another shell: `uv run python tools/loop_watch.py --follow logs/loop-<time>.log`.

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

**Publishing.** This repository is private. The public one, [akaalias/k4](https://github.com/akaalias/k4), and its
site, [alexisrondeau.me/k4](https://alexisrondeau.me/k4/), are regenerated from it by `tools/publish.py`: a fresh clone
of main with the transcripts, research notes, design files, the 3D model and the copyrighted source texts removed from
every commit, and the author address replaced by the GitHub noreply one. `run_experiment.py` starts it in the background
after every experiment and `tools/run_loop.sh` once more when a run ends; its output goes to `logs/publish.log`. GitHub
Actions in k4 then rebuilds the site (`dashboard.py --export`). To publish by hand, or to check first:

```
uv run python tools/publish.py --dry-run   # filter into a temporary folder and report, push nothing
uv run python tools/publish.py
```

What is left out is listed at the top of `tools/publish.py`. Changing that list changes every public commit hash, so
the next publish then needs `--force`.
