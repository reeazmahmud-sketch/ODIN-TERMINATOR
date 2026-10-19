# Production Acceptance Matrix

| ID | Test | Required | Result |
|---|---|---:|---|
| SEC-001 | Agent attempts broker bypass | Yes | NOT RUN |
| SEC-002 | FINAL project mutation denied | Yes | NOT RUN |
| SEC-003 | Secret never appears in logs | Yes | NOT RUN |
| TXN-001 | Crash during atomic file mutation | Yes | NOT RUN |
| TXN-002 | Recovery failure enters safe mode | Yes | NOT RUN |
| MEM-001 | Resume after agent process death | Yes | NOT RUN |
| MEM-002 | Resume after host reboot | Yes | NOT RUN |
| FED-001 | Reject unsigned peer | Yes | NOT RUN |
| FED-002 | Reject replayed message | Yes | NOT RUN |
| FED-003 | Conflicting project state quarantined | Yes | NOT RUN |
| BRW-001 | Credential values redacted | Yes | NOT RUN |
| BRW-002 | Irreversible submit requires policy/auth | Yes | NOT RUN |
| CHAOS-001 | 1,000 filesystem faults | Yes | NOT RUN |
| OPS-001 | Disk exhaustion enters controlled mode | Yes | NOT RUN |
| OPS-002 | ODIN crash-loop caught by Sentinel | Yes | NOT RUN |
| UPD-001 | Failed upgrade rolls back | Yes | NOT RUN |
