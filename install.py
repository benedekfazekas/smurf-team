#!/usr/bin/env python3
"""
Smurf Team installer.

Copies the Copilot agent files into the current git repository.

Usage:
  # Run directly
  python3 install.py

  # Or via curl (run from your repo root)
  curl -fsSL https://raw.githubusercontent.com/benedekfazekas/smurf-team/main/install.py | python3
"""

import argparse
import sys
import urllib.request
from pathlib import Path

REPO = "benedekfazekas/smurf-team"
BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

FILES = [
    ".github/agents/architect-smurf.agent.md",
    ".github/agents/brainy-smurf.agent.md",
    ".github/agents/grouchy-smurf.agent.md",
    ".github/agents/handy-smurf.agent.md",
    ".github/agents/README.md",
    ".github/agents/session_cost.py",
    ".github/instructions/caveman.instructions.md",
]


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def fetch(url: str) -> bytes:
    try:
        with urllib.request.urlopen(url) as resp:  # noqa: S310
            return resp.read()
    except Exception as exc:
        die(f"could not fetch {url}: {exc}")


def install(force: bool) -> None:
    cwd = Path.cwd()

    if not (cwd / ".git").exists():
        die("not a git repository root — cd into your repo first")

    skipped, written = [], []

    for rel in FILES:
        dest = cwd / rel
        if dest.exists() and not force:
            skipped.append(rel)
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        url = f"{BASE_URL}/{rel}"
        content = fetch(url)
        dest.write_bytes(content)
        written.append(rel)

    for f in written:
        print(f"  wrote  {f}")
    for f in skipped:
        print(f"  skip   {f}  (already exists — use --force to overwrite)")

    if not written:
        print("\nNothing written.")
    else:
        print(f"\nInstalled {len(written)} file(s).")
        print("\nNext steps:")
        print("  1. Create AGENTS.md at your repo root with project conventions")
        print("     (build cmd, test cmd, lint cmd, stack overview).")
        print("  2. Commit the new files.")
        print("  3. Start with:  copilot --agent brainy-smurf")
        print("     or see .github/agents/README.md for the full usage guide.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install Smurf Team agents into this repo.")
    parser.add_argument(
        "--force", action="store_true", help="overwrite existing files"
    )
    args = parser.parse_args()
    install(force=args.force)


if __name__ == "__main__":
    main()
