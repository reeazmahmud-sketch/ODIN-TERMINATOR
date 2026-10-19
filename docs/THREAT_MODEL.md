# Threat Model

## Protected assets
Project source, finished releases, credentials, policy, audit history, snapshots, node keys, agent state and user data.

## Trust boundaries
Human↔ODIN, TERMINATOR↔ODIN, worker↔broker, browser↔web, ODIN↔macOS privilege boundary, node↔node federation, updater↔installed runtime.

## Principal threats and required mitigations
- **Rogue/compromised agent:** capability allowlists, broker-only mutation, least privilege, rate limits.
- **Prompt/web injection:** browser content is untrusted data; page text cannot alter policy or authority.
- **Path traversal/symlink attacks:** canonicalize targets, enforce workspace roots, refuse unexpected links for destructive operations.
- **Replay/forged federation messages:** node signatures/mTLS, nonce, timestamp window, monotonic/version checks.
- **Audit tampering:** append-only records, hash chaining/signing, external rotation/retention.
- **Snapshot corruption:** content hashes, external snapshot vault, restore verification.
- **Disk exhaustion:** quotas, bounded logs/snapshots, reserve-space/safe-mode strategy.
- **Crash during mutation:** transaction journal + atomic writes + recovery on startup.
- **Bad update:** signed/pinned release, staged health check, automatic rollback.
- **Credential exfiltration:** Keychain, redaction, origin/action checks, no plaintext logging.
