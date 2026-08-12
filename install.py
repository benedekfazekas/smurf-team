#!/usr/bin/env python3
"""
Smurf Team installer.

Copies the Copilot agent files into the current git repository.

Usage:
  python3 install.py
"""

import argparse
import os
import ssl
import sys
import urllib.request
from pathlib import Path

REPO = "benedekfazekas/smurf-team"
BRANCH = os.environ.get("SMURF_BRANCH", "main")
BASE_URL = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

FILES = [
    ".github/agents/papa-smurf.agent.md",
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


def _ssl_context():
    """Return the best available SSL context."""
    # Try certifi first (most reliable cross-platform)
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    # macOS: load system keychain certs
    if sys.platform == "darwin":
        try:
            import subprocess
            result = subprocess.run(
                ["security", "find-certificate", "-a", "-p",
                 "/System/Library/Keychains/SystemRootCertificates.keychain"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout:
                import tempfile, os
                with tempfile.NamedTemporaryFile(mode="w", suffix=".pem", delete=False) as f:
                    f.write(result.stdout)
                    tmp = f.name
                try:
                    ctx = ssl.create_default_context(cafile=tmp)
                    return ctx
                finally:
                    os.unlink(tmp)
        except Exception:
            pass
    return ssl.create_default_context()


def fetch(url: str) -> bytes:
    ctx = _ssl_context()
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            return resp.read()
    except ssl.SSLCertVerificationError as exc:
        die(
            f"SSL certificate verification failed for {url}: {exc}\n"
            "  Refusing to continue — the downloaded agent files instruct an AI agent\n"
            "  that can run shell commands, so an unverified download is not safe.\n"
            "  Fix your certificate store, then re-run:\n"
            "    pip3 install certifi\n"
            "    (macOS) run 'Install Certificates.command' in your Python folder"
        )
    except Exception as exc:
        die(f"could not fetch {url}: {exc}")


def install(force: bool) -> None:
    cwd = Path.cwd()

    if not (cwd / ".git").exists():
        die(
            f"{cwd} is not a git repository root (no .git directory).\n"
            "  The installer writes into ./.github/ of the current directory, so run it\n"
            "  from the top level of the project you want the Smurf Team installed into:\n"
            "    cd /path/to/your/project && python3 install.py"
        )

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
        print("  1. Run Papa Smurf to generate AGENTS.md for your project:")
        print("       copilot --agent papa-smurf")
        print("  2. Review and commit the generated AGENTS.md.")
        print("  3. Start work:  copilot --agent brainy-smurf")
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
