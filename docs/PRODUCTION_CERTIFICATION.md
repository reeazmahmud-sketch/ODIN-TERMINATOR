# Production Certification

The implementation cannot be labeled production-ready until all release-blocking tests pass.

## Mandatory gates
- zero unauthorized destructive operations
- broker bypass tests fail closed
- policy precedence and malformed-policy tests pass
- 1,000+ isolated filesystem fault scenarios
- abrupt termination and Mac-restart recovery validated
- transaction and recovery verification validated
- secret-redaction tests pass
- federation authentication/replay/conflict tests pass
- corrupted snapshot/state database handling passes
- disk/memory pressure and bounded-log behavior passes
- ODIN and TERMINATOR crash recovery passes
- failed upgrade/downgrade recovery passes
- browser irreversible-action gates pass
- FINAL/ARCHIVED mutation attempts fail closed
- static analysis, type checks, unit/integration/chaos suites pass

A release candidate failing any security/recovery gate remains RC or experimental.
