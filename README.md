# ODIN + TERMINATOR
## Production Architecture & Engineering Specification

**Version:** 1.0.0-rc.1  
**Date:** 19-10-2026  
**Status:** Production Architecture / Implementation Specification — **not production-certified software**

ODIN + TERMINATOR is a governed multi-agent operating environment for macOS. TERMINATOR plans and orchestrates work; ODIN is the security and execution authority. No AI agent receives unrestricted permanent privilege.

## Non-negotiable invariants
1. Human authority remains supreme for privileged or destructive operations.
2. Every state-changing capability passes through the ODIN Capability Broker.
3. FINAL/ARCHIVED projects are immutable unless explicitly and time-boundedly unlocked.
4. Privileged eligibility is not privilege possession; macOS authorization is required at execution time.
5. Changes are transactional: capture pre-state → execute → verify → commit or recover.
6. Audit events are append-only; secrets and credential values are never logged.
7. Self-healing proposes or applies only bounded, verifiable repairs; it never silently rewrites unsafe state.
8. Pattern learning may recommend policy changes but never grants itself authority.
9. Federation uses authenticated nodes, signed/replay-resistant messages, versioned state and conflict resolution.
10. ODIN itself is supervised by a deterministic Sentinel and can enter safe mode.

## Architecture

```text
                     HUMAN
                       │
                 ultimate authority
                       │
                       ▼
                 TERMINATOR
             planning/orchestration
                       │
                       ▼
              ODIN CAPABILITY BROKER
                       │
     ┌─────────────────┼──────────────────┐
     ▼                 ▼                  ▼
  Identity        Project Guard        Policy
     └─────────────────┬──────────────────┘
                       ▼
                   Risk Engine
                 ┌─────┴─────┐
                 ▼           ▼
               ALLOW      HUMAN AUTH
                 └─────┬─────┘
                       ▼
               Transaction Engine
                       │
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
     macOS           Browser          Files/Agents
       └───────────────┬────────────────┘
                       ▼
                     VERIFY
                  ┌────┴────┐
                COMMIT    RECOVER
                  └────┬────┘
                       ▼
                  AUDIT JOURNAL
```

## Twenty-phase roadmap

| Phase | Area | Production requirement |
|---|---|---|
| 1 | Human Authority / Security Gate | Explicit human authorization for privileged operations |
| 2 | Dependency Graph + Break Detector | Pre-move/delete impact analysis and integrity detection |
| 3 | Controlled Self-Healing | Repair proposals/changes validated before commit |
| 4 | Policy Engine | Versioned, deny-by-default policy with deterministic precedence |
| 5 | Unified Dashboard | Nonblocking TUI using the same broker/event bus as CLI |
| 6 | Secure Browser Automation | Persistent sessions, action risk classes, secret redaction |
| 7 | Chaos & Resilience | Isolated fault injection; never damage production state |
| 8 | Multi-Mac Federation | mTLS/cryptographic identity, replay defense, reconciliation |
| 9 | Bounded Pattern Learning | Recommend policy; never self-authorize |
| 10 | Locked Demo + Reporting | Read-only sanitized views and weekly reports |
| 11 | Capability Broker / Kernel | Single controlled doorway for all state-changing actions |
| 12 | Transaction + Recovery | Durable pre-state, postcondition verification, recovery |
| 13 | Durable Memory + Resume | Checkpoints and safe restart after process/Mac failure |
| 14 | Native macOS Security | LocalAuthentication + supported authorization/TCC/SIP model |
| 15 | Cryptographic Node Identity | Signed node identity, nonce/timestamp/version checks |
| 16 | Secrets + Data Classification | Keychain-backed secrets, redaction, data handling classes |
| 17 | ODIN Sentinel / Safe Mode | Deterministic watchdog, crash-loop prevention, rollback |
| 18 | Observability + SLOs | Metrics, traces, audit correlation, bounded log growth |
| 19 | Install / Upgrade / Rollback | Pinned dependencies, signed artifacts, reversible upgrades |
| 20 | Production Certification | Acceptance suite must pass before production claim |

## Repository documentation
- `docs/ARCHITECTURE.md` — component boundaries and control plane
- `docs/SECURITY_MODEL.md` — authority, macOS controls, secrets and trust
- `docs/THREAT_MODEL.md` — assets, trust boundaries, threats and mitigations
- `docs/TRANSACTION_RECOVERY.md` — commit/recovery semantics
- `docs/DURABLE_MEMORY.md` — checkpoints and restart behavior
- `docs/MULTI_MAC_FEDERATION.md` — distributed-state design
- `docs/CHAOS_TESTING.md` — safe resilience testing
- `docs/OPERATIONS_RUNBOOK.md` — operational and safe-mode procedures
- `docs/PRODUCTION_CERTIFICATION.md` — release gate
- `schemas/` — canonical JSON schemas
- `policies/` — policy example
- `tests/PRODUCTION_ACCEPTANCE_MATRIX.md` — acceptance checklist

## Release rule
A release candidate can describe a production architecture. The software may be labeled **production-ready** only after the implementation passes the Production Certification Suite with zero unauthorized destructive operations and all required recovery/security tests passing.
