---
name: prompt-and-answer-dump
description: Append a visually separated, complete transcript of human and subagent prompts with their answers to an existing log file.
argument-hint: "LOG_FILE [summarise-answer]"
---

# Dump prompts and answers

Append a complete prompt/answer transcript from the **current session** to an existing log file.

## Arguments

Parse `$ARGUMENTS` as exactly:

```text
LOG_FILE [summarise-answer]
```

- `LOG_FILE` is required. It is the path of the existing regular log file to append to.
- `summarise-answer` is the only optional second argument. It is case-sensitive.
- Reject all other argument counts or values. Report the usage line and make no write.

## Validate before gathering

Validate `LOG_FILE` exactly once before reading the session history. Use this command, then write
the complete append through file descriptor `3` in that same shell:

```bash
if [ ! -e "$LOG_FILE" ]; then
  printf 'ERROR: %s: No such file or directory\n' "$LOG_FILE" >&2
  exit 1
fi
if [ ! -f "$LOG_FILE" ]; then
  printf 'ERROR: %s: not a regular file\n' "$LOG_FILE" >&2
  exit 1
fi
if ! exec 3>>"$LOG_FILE"; then
  exit 1  # Shell reports path and exact append-open error.
fi
```

This one pass checks:

1. It must exist.
2. It must be a regular file.
3. The agent must be able to open it for append.

If any validation or open fails, report an error that includes the path and exact OS/tool error
when available. Do not create the file. Do not truncate, overwrite, rename, or modify any existing
content. Do not attempt a partial append. Do not repeat this validation later in the same skill run.

## Capture scope

Capture every exchange already present in the current session, in chronological order:

1. Every **human prompt**: the complete user message, including timestamps, tagged-file blocks,
   and any other text supplied with it.
2. Every **assistant summary answer** to a human prompt: final user-facing answer only. Do not
   capture tool-call commentary, tool input/output, system notifications, developer instructions,
   or hidden reasoning.
3. Every **subagent prompt**: the complete text dispatched by the assistant to every subagent,
   including follow-up prompts sent to an existing subagent.
4. Every **subagent answer**: the complete response returned by that subagent for every dispatched
   prompt. Do not include transport metadata such as agent IDs, status, elapsed time, model
   labels, or the echoed prompt wrapper.

Prompts are immutable transcript records. Copy each human prompt and each subagent prompt
**verbatim**: preserve all characters, line breaks, Markdown, code fences, paths, punctuation,
and spelling. Never summarize, correct, normalize, redact, or omit prompt text.

For each prompt, retain the answer that followed it in the conversation. If a prompt has no answer
yet, append the prompt block followed by an explicit empty-answer marker:

```text
(No answer recorded yet.)
```

Do not invent missing conversation content. Gather from stored session history first. If it is
unavailable or incomplete (for example, it omits timestamps, tagged-file blocks, or recent exchanges),
use the visible transcript in the current conversation window to recover the missing records. Combine
both sources in chronological order, but include each exchange once only.

The visible transcript is authoritative for messages it shows. Copy its recoverable prompt and
answer content verbatim; do not infer or invent content not available in either source. Report the
limitation and make no write only when neither stored history nor the visible transcript can supply
a complete verbatim capture.

## Answer mode

### Default: verbatim answers

When `summarise-answer` is absent, copy every assistant summary answer and every subagent answer
**verbatim**, preserving all characters and line breaks.

### `summarise-answer`: compact answers

When the second argument is exactly `summarise-answer`:

- Keep every prompt verbatim; this mode never changes prompt capture.
- Replace every assistant summary answer and subagent answer with a factual summary of exactly
  **two sentences**.
- Use active caveman mode: terse fragments allowed, no filler, exact technical facts retained.
- Preserve exact identifiers, paths, test names, values, error messages, and command-result
  summary lines needed to understand the outcome.
- Do not add facts, decisions, caveats, or next steps absent from the original answer.
- An empty-answer marker remains unchanged; it is not summarized.

## Exact appended format

Append blocks only; preserve the log's existing contents byte-for-byte. Start each block after one
blank line. Use this exact 70-character separator and headings:

```text
══════════════════════════════════════════════════════════════════════
  HUMAN PROMPT N
══════════════════════════════════════════════════════════════════════

<verbatim human prompt>

══════════════════════════════════════════════════════════════════════
  ASSISTANT SUMMARY N
══════════════════════════════════════════════════════════════════════

<verbatim assistant final answer, or its two-sentence summary>
```

Use a single chronological counter `N` for each block type independently: human prompts numbered
`HUMAN PROMPT 1`, `HUMAN PROMPT 2`, and so on; assistant summaries numbered `ASSISTANT SUMMARY 1`,
`ASSISTANT SUMMARY 2`, and so on.

Use these distinct headings for subagent exchanges:

```text
══════════════════════════════════════════════════════════════════════
  SUBAGENT PROMPT N — <SUBAGENT DISPLAY NAME>
══════════════════════════════════════════════════════════════════════

<verbatim dispatched prompt>

══════════════════════════════════════════════════════════════════════
  SUBAGENT RESPONSE N — <SUBAGENT DISPLAY NAME>
══════════════════════════════════════════════════════════════════════

<verbatim subagent response, or its two-sentence summary>
```

Number subagent prompt and response blocks independently in chronological order. Use the
subagent's display name exactly as shown in the session, such as `HANDY SMURF`.

Human/assistant and subagent blocks must remain interleaved in the real chronological order in
which their messages occurred. The different headings make both role and direction obvious.

## Complete and report

After one successful append, report:

- exact log-file path;
- number of human prompts, assistant summaries, subagent prompts, and subagent responses appended;
- whether answers were `verbatim` or `summarise-answer`.

If writing fails, report the error and do not claim success.
