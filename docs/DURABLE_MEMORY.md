# Durable Memory & Crash Resume

Each task owns a durable state directory containing:

```text
intent.json
plan.json
context.json
decisions.json
actions.jsonl
artifacts.json
checkpoint.json
verification.json
recovery.json
```

Checkpoints are written only after verified boundaries. On restart ODIN detects incomplete transactions before allowing resume. `odin resume` must report the last verified checkpoint, pending work, integrity state and whether resume is safe. Agent conversational memory is not a substitute for this execution state.
