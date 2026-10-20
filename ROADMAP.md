# ODIN + TERMINATOR — Implementation Resume Roadmap

**Updated:** 19-10-2026  
**Purpose:** A short, durable checkpoint for resuming development without re-planning completed architecture.

## Current checkpoint

### Phase 11 — Capability Broker / Execution Kernel

Development continues on `phase-11-capability-broker` through Draft PR #1. Do not merge until the Phase 11 completion gate is satisfied.

Already established:

- immutable command envelopes;
- ordered governance gates: identity → Project Guard → policy → risk → authorization;
- fail-closed broker behavior;
- request-ID correlation checks;
- executor and audit boundaries;
- typed broker failures;
- initial unit tests and Phase 11 engineering specification.

### Resume here

When development resumes:

1. Inspect Draft PR #1 and the current Phase 11 branch before changing architecture.
2. Run the existing test suite and verify the branch state.
3. Continue with the first unfinished Phase 11 item below.
4. Do not redesign completed components unless testing or a security review identifies a concrete defect.

## Next implementation work

### Finish Phase 11

- [ ] Concrete identity adapter
- [ ] Concrete Project Guard adapter
- [ ] Policy evaluator adapter
- [ ] Risk classifier
- [ ] Verified interactive authorization continuation
- [ ] Explicit capability/action registry and allowlist
- [ ] Durable append-only audit storage with secret redaction
- [ ] External-boundary schema validation
- [ ] Idempotency and concurrency protection
- [ ] Integration tests using real adapters
- [ ] Lint, typecheck and automated test evidence in CI
- [ ] Security review
- [ ] Merge Phase 11 only after all mandatory gates pass

### Phase 12 — Transaction & Recovery Engine

Implement pre-action state capture, external recovery points, execute → verify → commit/recover semantics, interrupted-write protection, recovery validation and safe failure behavior.

### Phase 13 — Durable Memory & Crash Resume

Persist task state, plans, decisions, actions, artifacts and checkpoints. Implement `odin resume` and prove recovery after CLI/agent termination and host reboot without repeating completed work.

### Phases 14–17 — Security Hardening

- Native macOS security and privileged authorization
- Cryptographic node identity and federation security
- Secrets and data classification
- ODIN Sentinel and Safe Mode

### Phases 18–20 — Production Hardening

- Observability, health metrics and SLOs
- Installer, update, migration and rollback system
- Production certification and chaos/failure test suite

The system must not be labeled production-certified until the mandatory production acceptance matrix has objective passing evidence.

## Permanent engineering rules

- Human authority remains ultimate.
- TERMINATOR coordinates and requests capabilities; it does not bypass ODIN.
- Every governed capability enters through the ODIN Capability Broker.
- High trust never means permanent root access.
- Authorization-required actions remain suspended until verified authorization succeeds.
- Self-healing is bounded, policy-controlled and validated before commit.
- Filesystem watchers detect changes; they are not treated as authoritative write blockers.
- Recovery points must survive loss or replacement of the project being recovered.
- Private user authorization/control inputs must never be stored in documentation, source comments, commits, PR descriptions, issues, changelogs, normal logs or release notes.
- Credentials, tokens, passwords and biometric material must not enter ordinary logs or agent prompts.

## Definition of done

The development sequence is:

`build → test → security verify → integration verify → acceptance evidence → merge`

If there is uncertainty after a future restart, this file and the active Phase 11 PR are the canonical starting points.