---
name: summarize-session
description: Write a work summary for the current session. Optionally append it to an existing run and cost log file (produced by session_cost.py).
argument-hint: "[--log PATH]"
---

# Summarize the current session

Write a concise, factual **work summary** of what happened in this session, for the human who
orchestrated it. The summary is the narrative complement to the token/cost report produced by
`session_cost.py`; do **not** repeat or estimate token counts, costs, or timing — those come from
that script.

## Arguments

Parse `$ARGUMENTS`:

- No argument: print the summary in the response only.
- `--log PATH`: append the summary to the existing file at `PATH` after printing it.

The log path must point to an existing regular file. Never create, truncate, or overwrite it.
Append only. If the path does not exist or is not a regular file, report the error and skip the
write.

## Gather facts before writing

Run these commands to capture current workspace state. Quote exact output in the summary where
relevant.

```bash
git status --short
git diff --stat HEAD
```

If test or build commands are documented in `AGENTS.md`, report the last known result from this
session's conversation. Do not re-run them unless explicitly asked.

## What to write

The summary has one section. Model the **exact style** on this example (adapt sections to what
actually happened; omit sections with nothing truthful to say):

```
──────────────────────────────────────────────────────────────────────
  Session work summary (YYYY-MM-DD, human-orchestrated)
──────────────────────────────────────────────────────────────────────

  Context
  - Why this session started; what problem or goal the human brought.

  Plan / approach   (omit if no planning happened)
  - Key design decisions, rejected alternatives, constraints adopted.

  Plan review findings   (omit if no review happened)
  - F-001 (major): ...
  - F-002 (withdrawn): ...

  Work completed
  - Exact files changed, functions renamed, tests added.
  - Test run outcome: N passed, N skipped, N failed (quote the runner line).

  Bugs fixed / regressions caught   (omit if none)
  - What was wrong, what the fix was, how it was verified.

  Left open / next actions   (omit if none)
  - What was not done, what the human should do next.
```

Rules:
- Use the **exact** date this session ran (obtain with `date -u +%Y-%m-%d`).
- Use exact file paths, symbol names, function names, test counts.
- Never invent facts not present in the conversation or command output.
- Each bullet: one to two lines. No prose paragraphs.
- Do not include token counts, cost, timing, or model names — those belong in the
  `session_cost.py` report, not here.

## Appending to a log file

When `--log PATH` is given, append the summary block to the file after printing it in the
response. Preserve everything already in the file. Confirm the append in your response with the
path. If the write fails, quote the exact error and do not claim the log was updated.
