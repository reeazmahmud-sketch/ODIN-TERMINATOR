# Transaction & Recovery

A rollback is valid only when ODIN has enough typed pre-state to compensate or restore the operation.

```text
BEGIN → validate → capture pre-state → recovery point → execute → verify
                                                       ├─ PASS → COMMIT
                                                       └─ FAIL → RECOVER → VERIFY RECOVERY
```

## Rules
- Use atomic write-to-temp + fsync + rename for critical state files.
- Snapshots live outside the project being restored.
- Snapshot manifests are deterministic and exclude mutable caches/logs/venvs/build output.
- Irreversible operations are marked `irreversible`; ODIN must not invent an “undo”.
- Browser actions are classified as reversible, compensatable or irreversible.
- Recovery failure immediately enters safe mode and blocks further mutations for the affected scope.
