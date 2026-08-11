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
import ssl
import sys
import urllib.request
from pathlib import Path

REPO = "benedekfazekas/smurf-team"
BRANCH = "main"
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
    import ssl
    # Try certifi first (most reliable cross-platform)
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    # macOS: load system keychain certs
    if sys.platform == "darwin":
        ctx = ssl.create_default_context()
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
    import ssl
    ctx = _ssl_context()
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            return resp.read()
    except ssl.SSLCertVerificationError:
        print("warning: SSL verification failed — retrying without verification", file=sys.stderr)
        print("         (fix: run `pip3 install certifi` or on macOS run the", file=sys.stderr)
        print("          'Install Certificates.command' in your Python folder)", file=sys.stderr)
        ctx_noverify = ssl.create_default_context()
        ctx_noverify.check_hostname = False
        ctx_noverify.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(req, context=ctx_noverify) as resp:
                return resp.read()
        except Exception as exc:
            die(f"could not fetch {url}: {exc}")
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
