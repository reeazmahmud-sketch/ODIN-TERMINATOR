"""Fail-closed ODIN Capability Broker skeleton.

Phase 11 establishes the mandatory execution doorway. Concrete identity,
project, policy, authorization, transaction and audit adapters are injected;
the broker never grants itself authority.
"""
from __future__ import annotations

from typing import Protocol

from .models import BrokerDecision, CommandEnvelope, Decision


class Gate(Protocol):
    def evaluate(self, request: CommandEnvelope) -> BrokerDecision: ...


class CapabilityExecutor(Protocol):
    def execute(self, request: CommandEnvelope) -> object: ...


class AuditSink(Protocol):
    def record(self, request: CommandEnvelope, decision: BrokerDecision) -> None: ...


class CapabilityBroker:
    """Routes every supported capability through ordered governance gates."""

    def __init__(
        self,
        *,
        identity: Gate,
        project_guard: Gate,
        policy: Gate,
        risk: Gate,
        authorization: Gate,
        executor: CapabilityExecutor,
        audit: AuditSink,
    ) -> None:
        self._gates = (identity, project_guard, policy, risk, authorization)
        self._executor = executor
        self._audit = audit

    def dispatch(self, request: CommandEnvelope) -> object:
        for gate in self._gates:
            decision = gate.evaluate(request)
            self._audit.record(request, decision)
            if decision.decision is Decision.DENY:
                raise PermissionError(decision.reason)
            if decision.decision is Decision.REQUIRE_AUTH:
                raise PermissionError(
                    "interactive authorization is required before execution"
                )

        # Execution is reached only when every gate explicitly allows.
        result = self._executor.execute(request)
        self._audit.record(
            request,
            BrokerDecision(Decision.ALLOW, "execution completed", request.request_id),
        )
        return result
