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

**Create `AGENTS.md` at your repo root.** The agents read this file first on every engagement to learn your project's conventions — build command, test command, lint command, stack overview. Without it the agents will ask you for this information each time.

Minimal example:

```markdown
# AGENTS.md

## Build
./gradlew build

## Test
./gradlew test

## Lint
./gradlew ktlintCheck

## Stack
Kotlin, Spring Boot, Gradle, Kubernetes (Helm), GCP
```

Commit the new files and you are done.

## Usage

```bash
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
