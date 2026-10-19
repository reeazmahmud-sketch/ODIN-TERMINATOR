# Architecture

## Roles
**Human:** ultimate authority.  
**TERMINATOR:** high-level planner/orchestrator. It requests capabilities; it does not bypass ODIN.  
**ODIN Core:** policy/security/execution authority.  
**Agents:** bounded workers with declared capabilities.  
**Sentinel:** deterministic, non-AI supervisor for ODIN health and safe mode.

## Capability request envelope
Every mutating request includes `request_id`, `actor_id`, `node_id`, `project_id`, `capability`, `action`, typed `args`, `intent_hash`, timestamp, risk class, and authentication context. Federation adds nonce/signature/version.

## Execution sequence
1. Validate schema and freshness.
2. Authenticate actor/node.
3. Resolve project lifecycle state.
4. Evaluate capability and policy.
5. Classify risk and data sensitivity.
6. Obtain human authorization when required.
7. Begin transaction and capture recoverable pre-state.
8. Execute typed capability without `shell=True` for untrusted input.
9. Verify postconditions, integrity and required tests.
10. Commit or recover.
11. Append correlated audit records.

## Project lifecycle
`ACTIVE → FROZEN → FINAL → ARCHIVED`. FINAL/ARCHIVED are deny-write by default. Editing a FINAL project creates an explicit working copy/worktree rather than silently unlocking the original.

## Dashboard
CLI, TUI and automation clients consume the same broker and event bus. The TUI must never call an infinite CLI command through blocking `subprocess.run`; event streaming is asynchronous and bounded.

## Optional TUI enhancements retained
- paging/scrollback beyond 20 incidents
- `+/-` refresh controls
- persistent domain filters
- multi-column advanced metrics
