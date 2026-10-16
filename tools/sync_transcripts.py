"""Mirror this project's Claude Code transcripts and agent logs into transcripts/ (issue: keep every chat).

Source: ~/.claude/projects/<this project's slug>/ — one .jsonl per session (the chats, including the
harness's own model calls), <session>/subagents/*.jsonl and *.meta.json (the internal agent logs),
<session>/tool-results/ (large tool outputs the transcripts point at).

Each .jsonl is split into parts of PART_LINES lines and gzipped with a fixed timestamp, so a part that
has not changed produces identical bytes and git stores it once; only the newest part of a growing log
changes between syncs. This also keeps every file far below GitHub's 100 MB limit.

    uv run python tools/sync_transcripts.py            # mirror
    uv run python tools/sync_transcripts.py --commit   # mirror, commit and push if anything changed
    uv run python tools/sync_transcripts.py --commit --every 20   # the same, at most once per 20 minutes

The project's .claude/settings.json runs it from hooks: after every turn (throttled, in the background),
before every context compaction and at the end of every session.
"""

import gzip
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path.home() / ".claude" / "projects" / ("-" + str(ROOT).strip("/").replace("/", "-"))
DST = ROOT / "transcripts"
PART_LINES = 200
STAMP = ROOT / ".transcripts_sync"          # last sync time; gitignored


def write_gz(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(data)


def mirror_jsonl(src, rel):
    lines = src.read_bytes().splitlines(keepends=True)
    parts = [lines[i:i + PART_LINES] for i in range(0, len(lines), PART_LINES)] or [[]]
    wanted = set()
    for k, chunk in enumerate(parts):
        out = DST / rel.parent / f"{rel.stem}.part{k:03d}.jsonl.gz"
        wanted.add(out)
        data = b"".join(chunk)
        if out.exists():
            with gzip.open(out, "rb") as f:
                if f.read() == data:
                    continue
        write_gz(out, data)
    return wanted


def main():
    if "--every" in sys.argv:
        minutes = float(sys.argv[sys.argv.index("--every") + 1])
        if STAMP.exists() and time.time() - STAMP.stat().st_mtime < minutes * 60:
            return
    STAMP.touch()
    if not SRC.exists():
        sys.exit(f"no transcripts at {SRC}")
    keep = set()
    for src in sorted(SRC.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(SRC)
        if rel.parts[0] == "memory":
            out = DST / rel                      # the assistant's memory notes, as plain text
            keep.add(out)
            if not out.exists() or out.read_bytes() != src.read_bytes():
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, out)
        elif src.suffix == ".jsonl":
            keep |= mirror_jsonl(src, rel)
        else:
            out = DST / rel.parent / (rel.name + ".gz")
            keep.add(out)
            data = src.read_bytes()
            if out.exists():
                with gzip.open(out, "rb") as f:
                    if f.read() == data:
                        continue
            write_gz(out, data)
    for old in DST.rglob("*"):
        if old.is_file() and old not in keep and old.name != "README.md":
            old.unlink()
    if "--commit" in sys.argv:
        git = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
        git("add", "-A", "transcripts")
        if git("diff", "--cached", "--quiet", "--", "transcripts").returncode != 0:
            git("commit", "-m", "Transcripts and agent logs synced", "--", "transcripts")
            git("pull", "--rebase", "--autostash")
            git("push")


if __name__ == "__main__":
    main()
