# Chaos & Resilience Testing

Chaos tests run only in isolated fixtures/sandboxes by default. They must never disable the user's real network interface, corrupt production policy or delete real project files.

Required scenarios include file deletion/move simulation, interrupted atomic writes, CPU/memory/disk pressure with hard limits, process crashes, denied authorization, malformed policy, snapshot corruption, federation disconnect/replay, browser hazard pages, ODIN/TERMINATOR crashes and upgrade failure.

Retained advanced scenarios: simultaneous incidents, intermittent failures, fix→recover→re-fix chains, response-time measurement and high-frequency TUI event validation.
