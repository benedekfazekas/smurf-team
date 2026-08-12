# AGENTS.md

## Build

No build step. Pure Python (3.6+), no compilation.

## Test

No test suite configured.

## Lint

None configured.

## Stack

- **Language:** Python 3.6+
- **Framework:** None (stdlib only — `urllib`, `argparse`, `pathlib`)
- **CI:** None configured
- **Infra:** None — this repo is distributed via `curl | python3`

## Key directories

- `install.py` — single-file installer; fetches agent files from GitHub and writes them into a target repo
- `.github/agents/` — the Copilot custom agent definitions (`.agent.md` files) and supporting tools
- `.github/instructions/` — Copilot instruction files (`caveman.instructions.md`)

## Conventions

- No branch strategy documented. No PR template.
- The repo **is** the Smurf Team installer. It does not use the Smurf Team workflow on itself.
- To test installer changes against a branch: `SMURF_BRANCH=<branch> python3 install.py --force`
- Agent files under `.github/agents/` are the canonical source fetched by `install.py`; keep them consistent with `FILES` list in `install.py`.

### Git commit conventions

- Title + one sentence body (or a short bullet list for multi-fix commits)
- Do **not** mention Copilot or AI in the message
- if working locally and on the `main` branch the user controls what is staged before committing
- if working on a github issue always put a reference of the issue in the commit message
- never push directly on the `main` branch
