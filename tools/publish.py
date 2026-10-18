"""Publish the public repository akaalias/k4 from this private one (issue #66).

This repository stays private and is where the loop works. The public one is regenerated from it:
a fresh clone of main, with git filter-repo removing from every commit what may not be published,
then pushed to k4. Its GitHub Actions workflow builds the site from it (dashboard.py --export) and
serves it at https://alexisrondeau.me/k4/.

Left out of every commit:
  transcripts/        the chat transcripts and agent logs (personal; they also hold page images)
  research_notes/     the raw notes behind the reports, which quote their sources at length
  design/             style guides and illustration directions
  assets/kryptos.glb  Bret L Bowen's model: only his own zip may be redistributed
  knowledge/sources/  the full texts, except the public-domain ones in SOURCES_PUBLIC and the
                      index, which says where to read every original

The author address becomes the GitHub noreply one. Filtering the same history the same way gives
the same commits, so each publish fast-forwards k4; a change to the rules above changes every hash
and needs --force once.

    uv run python tools/publish.py            # publish main as it is now
    uv run python tools/publish.py --dry-run  # filter into a temp folder and report, push nothing
    uv run python tools/publish.py --force    # after changing the rules above

run_experiment.py starts it in the background after every experiment; a run that finds another
one in progress leaves a note, and the running one goes round again when it ends.
"""

import argparse
import fcntl
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = "https://github.com/akaalias/k4.git"
LOCK = ROOT / ".publish.lock"            # gitignored
AGAIN = ROOT / ".publish.again"          # gitignored: main moved while a publish was running
MAILMAP = "Alexis Rondeau <111555+akaalias@users.noreply.github.com> <alexis.rondeau@gmail.com>\n"

DROP_DIRS = ("transcripts/", "research_notes/", "design/")
DROP_FILES = ("assets/kryptos.glb",)
SOURCES_PUBLIC = (
    "INDEX.md",
    "army-1950-tm32-220-basic-cryptography.txt",
    "bauer-2017-unsolved-chapter-notes.md",
    "carter-1923-tomb-of-tutankhamen-vol1.txt",
    "cia-legacy-page.txt",
    "friedman-1935-elementary-military-cryptography.txt",
    "friedman-1943-elementary-military-cryptography.txt",
    "lewis-nsa-german-agent-systems-wwii.pdf",
    "lewis-nsa-german-agent-systems-wwii.txt",
    "nsa-1954-basic-cryptologic-glossary.txt",
    "nsa-1955-basic-cryptologic-glossary-draft.txt",
    "nsa-2014-summary-of-previous-work.txt",
    "nsa-foia-1992-2014-blackvault-compilation.txt",
    "wikipedia-kryptos-wikitext-2026-10.txt",
)

CALLBACK = f"""
name = filename.decode()
if name.startswith({DROP_DIRS!r}) or name in {DROP_FILES!r}:
    return None
if name.startswith("knowledge/sources/") and name[len("knowledge/sources/"):] not in {SOURCES_PUBLIC!r}:
    return None
return filename
"""


def run(*cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def publish_once(dry_run, force):
    head = subprocess.run(["git", "rev-parse", "main"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="k4-publish-") as tmp:
        work = Path(tmp) / "k4"
        run("git", "clone", "-q", "--no-local", "--single-branch", "--branch", "main", str(ROOT), str(work))
        (Path(tmp) / "mailmap").write_text(MAILMAP)
        run("uvx", "--quiet", "--from", "git-filter-repo", "git-filter-repo", "--quiet", "--force",
            "--filename-callback", CALLBACK, "--mailmap", str(Path(tmp) / "mailmap"), cwd=work)
        n = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=work, capture_output=True, text=True).stdout.strip()
        if dry_run:
            size = subprocess.run(["du", "-sh", str(work / ".git")], capture_output=True, text=True).stdout.split()[0]
            print(f"would publish {head[:7]}: {n} commits, .git {size}")
            return head
        run("git", "push", "-q", *(["--force"] if force else []), PUBLIC, "HEAD:main", cwd=work)
        print(f"published {head[:7]} to k4 ({n} commits)")
    return head


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    with open(LOCK, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            AGAIN.touch()
            print("a publish is already running; it will go round again when it ends")
            return
        while True:
            AGAIN.unlink(missing_ok=True)
            publish_once(a.dry_run, a.force)
            if a.dry_run or not AGAIN.exists():
                break


if __name__ == "__main__":
    sys.exit(main())
