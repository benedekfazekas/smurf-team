# Install Smurf Team

Adds four Copilot custom agents — Brainy, Architect, Handy, and Grouchy — to any existing GitHub repository.

## Prerequisites

- Python 3.6+
- A GitHub repository (local clone with `.git` present)
- GitHub Copilot with agent support (Copilot Pro or Enterprise)

## Install

Run from your **repo root**:

```bash
curl -fsSL https://raw.githubusercontent.com/benedekfazekas/smurf-team/main/install.py | python3
```

Or download and run:

```bash
curl -fsSL https://raw.githubusercontent.com/benedekfazekas/smurf-team/main/install.py -o install.py
python3 install.py
# optionally remove the script after
rm install.py
```

To overwrite files that already exist:

```bash
curl -fsSL https://raw.githubusercontent.com/benedekfazekas/smurf-team/main/install.py | python3 - --force
```

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
.github/instructions/
  caveman.instructions.md      ← terse output mode (optional, harmless)
```

Nothing in your codebase is modified. All files land under `.github/`.

## After install

**Run Papa Smurf** to auto-generate `AGENTS.md` for your project:

```bash
copilot --agent papa-smurf
```

Papa Smurf starts onboarding on your first message — no special phrase needed. He explores the
repo, discovers your build/test/lint commands and stack, asks a few targeted questions for anything
he can't infer, then writes and commits `AGENTS.md`. Run him once — after that the rest of the
team takes over.

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

## Developing on a branch

When working on changes to the installer or agent files, test against your branch before merging to `main`:

```bash
BRANCH=your-branch-name

curl -fsSL https://raw.githubusercontent.com/benedekfazekas/smurf-team/$BRANCH/install.py \
  | SMURF_BRANCH=$BRANCH python3 - --force
```

`SMURF_BRANCH` tells the installer to fetch all agent files from that branch instead of `main`.
Without it, the installer always pulls from `main` regardless of where `install.py` itself came from.
