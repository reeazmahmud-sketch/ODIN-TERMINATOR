# ODIN + TERMINATOR — Production Architecture & Engineering Specification

**Version:** 1.0.0-rc.1  
**Date:** 19-10-2026  
**Status:** Production Architecture / Implementation Specification  
**Certification:** NOT YET PRODUCTION-CERTIFIED

ODIN + TERMINATOR is a production-target architecture for a resilient, policy-governed multi-agent control system.

- **TERMINATOR** is the high-level AI orchestrator. It plans, delegates, coordinates, and requests capabilities.
- **ODIN** is the security and execution authority. It validates identity, project state, policy, risk, authorization, transactions, verification, recovery, and audit.
- **Human authority remains ultimate.** No AI agent receives a permanent bypass around policy or privileged authorization.

## Core invariant

```text
Human / TERMINATOR / Agents / Voice
                 |
                 v
        ODIN Capability Broker
                 |
    Identity -> Project Guard -> Policy -> Risk -> Auth
                 |
                 v
          Transaction Engine
                 |
                 v
            Capability
     macOS / Browser / Files / Agents
                 |
                 v
              Verify
            /        \
        Commit      Recover
            \        /
                 v
              Audit
```

No supported capability is allowed to bypass this pipeline.

## Production roadmap

1. Human Authority & Security Gate
2. Dependency Graph & Break Detector
3. Controlled Self-Healing
4. Policy Engine / `odin.policy`
5. Unified ODIN + TERMINATOR Dashboard
6. Secure Browser Automation
7. Chaos & Resilience Testing
8. Multi-Mac Federation
9. Bounded Agent Pattern Learning
10. Locked Demo Mode + Automated Reporting
11. Capability Broker / Execution Kernel
12. Transaction & Recovery Engine
13. Durable Memory + Crash Resume
14. Native macOS Security Layer
15. Cryptographic Node Identity & Federation Security
16. Secrets & Data Classification
17. ODIN Sentinel / Safe Mode
18. Observability, Health Metrics & SLOs
19. Installation, Updates, Migration & Rollback
20. Production Certification Suite

## Repository map

- `docs/ARCHITECTURE.md` — authority boundaries and execution architecture
- `docs/SECURITY_MODEL.md` — security invariants and macOS security model
- `docs/THREAT_MODEL.md` — assets, threats, mitigations and trust boundaries
- `docs/TRANSACTION_RECOVERY.md` — crash-safe transaction and rollback model
- `docs/DURABLE_MEMORY.md` — persistent task state and restart/resume design
- `docs/MULTI_MAC_FEDERATION.md` — zero-trust multi-node coordination
- `docs/CHAOS_TESTING.md` — safe resilience testing strategy
- `docs/OPERATIONS_RUNBOOK.md` — operator procedures and safe mode
- `docs/PRODUCTION_CERTIFICATION.md` — release gates
- `schemas/` — canonical command, event, project and federation schemas
- `policies/odin.policy.example` — policy example
- `tests/PRODUCTION_ACCEPTANCE_MATRIX.md` — certification evidence matrix

## Project lifecycle

ODIN recognizes four project states:

`ACTIVE -> FROZEN -> FINAL -> ARCHIVED`

`FINAL` and `ARCHIVED` projects are immutable through normal agent operations. Mutation requires an explicit, policy-authorized unlock flow. A high-trust agent may request privileged work but never bypass that flow.

## Trust levels

| Level | Meaning |
|---|---|
| L0 | Read only |
| L1 | Safe write |
| L2 | Code write |
| L3 | System-write capabilities where policy permits |
| L4 | Eligible to request privileged actions; **not** permanent root |

## Important safety corrections

This specification intentionally rejects several unsafe prototype assumptions:

- A filesystem watcher detects changes; it is not treated as an authoritative write blocker.
- Snapshots/recovery points must not depend on storage inside the project being replaced.
- Repeated human approval never automatically grants higher privilege.
- Self-healing changes require bounded scope, validation and policy permission before commit.
- Touch ID/user presence and macOS privileged authorization are separate security mechanisms.
- Browser credentials/tokens must not enter normal logs or agent prompts.
- TERMINATOR has no direct privileged bypass around ODIN.
- Destructive operations require recoverability classification and transaction handling.

## Release status

`v1.0.0-rc.1` is a **documentation release candidate**. The architecture may be used to guide implementation, but the software must not be represented as production-certified until the acceptance matrix has objective evidence for every mandatory gate.

See `docs/PRODUCTION_CERTIFICATION.md` and `tests/PRODUCTION_ACCEPTANCE_MATRIX.md`.
