# Audit

How to audit this repo, for a person or a coding agent. A report, not a change: no code edits.

## 1. This project's high-cost areas

Fill this in once per project. Audit these first and deepest.

| Area | Why a mistake here is expensive | Proof it works |
|---|---|---|
| _e.g. train vs deploy preprocessing_ | _policy scores in sim, fails on the robot_ | _parity test feeding the same input to both_ |
| _e.g. eval scoring_ | _a wrong number decides which model ships_ | _failed or hung trials count as failures_ |
| _e.g. HTTP routes that start processes or write files_ | _anyone on the network can run code_ | _binds 127.0.0.1, inputs checked_ |

Expected load: _one person on one machine / a lab network / many users_. Judge scale against it.

## 2. Map first

- Read the README, build and deploy config, dependencies, entry points (CLI commands,
  routes, jobs) and tests.
- Trace each main flow end to end: where data comes in, what is stored, what goes out.
- Big repo: split by area (e.g. core logic / deploy path / UI and tooling), go deep
  where mistakes cost most, and list what you did not read.

## 3. Look for, in this order

1. **Bug**: wrong result, crash, missed edge case (empty, zero, first/last item, reset,
   restart, time zones), two copies of one rule that disagree.
2. **Risk**: unchecked input from users or the network, injection, files written
   outside their folder, errors swallowed, results overwritten or mixed between runs.
3. **Scale**: races between two requests, memory that only grows, work repeated per item.
4. **Missing test**: risky logic that no test would catch breaking.
5. **Speed**: big slowdowns only.
6. **Lean**: dead code (grep the whole tree first), duplicates, options nobody sets.

## 4. Check before reporting

- Every finding has a concrete case: this input or situation gives this wrong result.
- Prove it with a probe script or a run when cheap; mark each finding run or read-only.
- `shortcut:` comments are decisions, not findings, unless the expected load crosses them.
- Smallest fix that works; prefer fixes that delete code.
- No style taste, no "consider", no vague worries.

## 5. Report format

Start with `What this repo does:` (two or three sentences) and the load assumed.
Group findings as **Must fix** (bug, security, data loss), **Should fix**, **Nice to have**.
Number them across groups. Each finding:

```
3. **Short title** (`path/file.py:L40-52`)
   - **What this is:** what the code does, for a reader who never saw it.
   - **Problem:** the concrete failing case.
   - **Fix:** the smallest change.
   - **If we skip it:** what goes wrong, for whom.
```

End with `Verdict:`, `Lean: -N lines possible` if any, and `Not checked:`.
