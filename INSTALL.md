# Install Smurf Team

Adds four Copilot custom agents — Brainy, Architect, Handy, and Grouchy — to any existing GitHub repository.

## Prerequisites

- Python 3.6+
- A GitHub repository (local clone with `.git` present)
- GitHub Copilot with agent support (Copilot Pro or Enterprise)

## Install

Run from your **repo root**.

### Option 1 — Download, inspect, run (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/benedekfazekas/smurf-team/main/install.py -o install.py
less install.py          # under 200 lines, no eval, writes only under .github/
python3 install.py
rm install.py
```

To overwrite files that already exist:

```bash
python3 install.py --force
```

### Option 2 — Clone and copy (zero trust in a script)

Fully equivalent to Option 1; `cp` overwrites instead of `--force`:

```bash
rm -rf /tmp/smurf-team
git clone --depth 1 https://github.com/benedekfazekas/smurf-team.git /tmp/smurf-team
mkdir -p .github
cp -r /tmp/smurf-team/.github/agents /tmp/smurf-team/.github/instructions .github/
```

### Option 3 — Branch testing

When working on changes to the installer or agent files, test against your branch before merging to `main`:

```bash
BRANCH=your-branch-name

curl -fsSL https://raw.githubusercontent.com/benedekfazekas/smurf-team/$BRANCH/install.py -o install.py
SMURF_BRANCH=$BRANCH python3 install.py --force
rm install.py
```

`SMURF_BRANCH` tells the installer to fetch all agent files from that branch instead of `main`.
Without it, the installer always pulls from `main` regardless of where `install.py` itself came from.

### Security

The installer transfers files only over verified TLS and aborts if verification fails — it will
never proceed with an unverified connection. The files it writes are AI agent instructions for a
Copilot agent with shell access; treat them with the same scrutiny you would apply to any
third-party dependency.

## What gets installed

```
.github/agents/
  papa-smurf.agent.md          ← onboarding agent (run once after install)
  brainy-smurf.agent.md        ← orchestrator (cheap model, routes everything)
  architect-smurf.agent.md     ← architect (expensive, plans + gates)
  handy-smurf.agent.md         ← developer (implements)
  grouchy-smurf.agent.md       ← reviewer (tester + technical writer)
  README.md                    ← team playbook
  session_cost.py              ← token/cost reporting tool
.github/skills/
  summarize-session/SKILL.md    ← current-session summary and optional log append
.github/instructions/
  caveman.instructions.md      ← terse output mode (optional, harmless)
```

Nothing in your codebase is modified. All files land under `.github/`.

## After install

**Run Papa Smurf** to auto-generate `AGENTS.md` for your project:

```bash
copilot --agent papa-smurf
```

When the session opens, say **`La la la!`** — Papa Smurf starts onboarding immediately.

## Usage

```bash
copilot --agent papa-smurf       # run once after install — generates AGENTS.md
copilot --agent brainy-smurf     # full orchestrated workflow
copilot --agent architect-smurf  # design question or diagnosis only
copilot --agent handy-smurf      # small, well-scoped implementation
copilot --agent grouchy-smurf    # one-off review
```

Inside an existing Copilot session:

```
/agent brainy-smurf
```

See `.github/agents/README.md` for the full team playbook, flow diagram, and cost-reporting instructions.
