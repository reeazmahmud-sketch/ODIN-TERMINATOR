# Operations Runbook

## Safe mode triggers
Policy integrity failure, repeated ODIN crash, transaction recovery failure, audit-store corruption, node identity failure, severe disk pressure or failed upgrade health check.

## Safe mode behavior
Block mutations; preserve read-only diagnostics; stop nonessential agents; rotate/cap logs safely; expose recovery status; require explicit human authorization to exit after health checks pass.

## Sentinel
Sentinel is deterministic and minimal—not an AI agent. It health-checks ODIN, detects crash loops, verifies critical policy/config hashes, bounds logs, starts safe mode and can roll back a failed ODIN release.
