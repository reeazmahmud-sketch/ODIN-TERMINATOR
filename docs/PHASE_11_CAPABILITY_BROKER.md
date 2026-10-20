# Phase 11 — ODIN Capability Broker / Execution Kernel

**Status:** Implementation in progress  
**Production certification:** Not yet certified

## Purpose

Phase 11 creates one mandatory doorway for every governed capability. TERMINATOR and subordinate agents may request work, but they do not call privileged capability implementations directly.

## Execution order

```text
request
  -> identity
  -> project guard
  -> policy
  -> risk
  -> authorization
  -> capability executor
  -> completion audit
```

Every gate must explicitly return `ALLOW`. `DENY`, `REQUIRE_AUTH`, gate exceptions, request-correlation failures, and audit failures stop execution.

## Security invariants

1. The broker never grants itself authority.
2. No trust level is equivalent to permanent root access.
3. Authorization-required work is suspended rather than executed.
4. The request identifier must remain stable across all governance decisions.
5. An unavailable governance gate fails closed.
6. An unavailable audit boundary blocks execution rather than producing an unaudited action.
7. Executor exceptions are recorded as failures and propagated to the caller.
8. Request metadata must not contain private approval phrases, credentials, tokens, passwords, or biometric material.
9. Project lifecycle rules remain authoritative for `FINAL` and `ARCHIVED` projects.
10. Phase 12 owns transaction/recovery semantics; Phase 11 must not pretend an executor failure has been rolled back unless Phase 12 proves recovery.

## Current implementation

The Python broker defines:

- immutable command envelopes;
- explicit governance decisions;
- named ordered gates;
- fail-closed exception handling;
- request-ID correlation checks;
- an executor interface;
- an audit interface;
- typed broker failures;
- unit tests for allow, deny, authorization-required, gate failure, correlation failure, audit failure, executor failure, and invalid requests.

## Remaining before Phase 11 can be called complete

- concrete identity adapter;
- concrete Project Guard adapter;
- real policy evaluator;
- risk classifier;
- verified interactive authorization continuation;
- capability registry with explicit allowlisted actions;
- durable append-only audit implementation with secret redaction;
- schema validation at external boundaries;
- concurrency/idempotency controls;
- integration tests using real adapters;
- lint, typecheck and test evidence in CI.

Transaction snapshots, rollback, postcondition verification and crash recovery are intentionally assigned to Phase 12 and must integrate through the broker rather than bypass it.
