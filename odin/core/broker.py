"""Fail-closed ODIN Capability Broker.

Every supported capability must enter through this broker. Governance failures,
audit failures, and executor failures never become implicit approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from .models import (
    BrokerDecision,
    CommandEnvelope,
    Decision,
    DispatchOutcome,
    DispatchStatus,
)


class BrokerError(RuntimeError):
    """Base class for broker failures."""


class RequestDenied(BrokerError):
    pass


class AuthorizationRequired(BrokerError):
    pass


class GovernanceFailure(BrokerError):
    pass


class AuditFailure(BrokerError):
    pass


class ExecutionFailure(BrokerError):
    pass


class Gate(Protocol):
    def evaluate(self, request: CommandEnvelope) -> BrokerDecision: ...


class CapabilityExecutor(Protocol):
    def execute(self, request: CommandEnvelope) -> object: ...


class AuditSink(Protocol):
    def record(self, request: CommandEnvelope, decision: BrokerDecision) -> None: ...


@dataclass(frozen=True, slots=True)
class NamedGate:
    name: str
    gate: Gate


class CapabilityBroker:
    """The mandatory execution doorway for governed capabilities."""

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
        self._gates: Sequence[NamedGate] = (
            NamedGate("identity", identity),
            NamedGate("project_guard", project_guard),
            NamedGate("policy", policy),
            NamedGate("risk", risk),
            NamedGate("authorization", authorization),
        )
        self._executor = executor
        self._audit = audit

    def _record(self, request: CommandEnvelope, decision: BrokerDecision) -> None:
        try:
            self._audit.record(request, decision)
        except Exception as exc:
            # Audit is part of the security boundary. If evidence cannot be
            # recorded, execution must not continue.
            raise AuditFailure("audit sink unavailable; request blocked") from exc

    def dispatch(self, request: CommandEnvelope) -> DispatchOutcome:
        for named in self._gates:
            try:
                raw = named.gate.evaluate(request)
            except Exception as exc:
                raise GovernanceFailure(f"{named.name} gate failed closed") from exc

            if raw.request_id != request.request_id:
                raise GovernanceFailure(f"{named.name} returned a mismatched request id")

            decision = BrokerDecision(
                decision=raw.decision,
                reason=raw.reason,
                request_id=raw.request_id,
                gate=named.name,
            )
            self._record(request, decision)

            if decision.decision is Decision.DENY:
                raise RequestDenied(decision.reason)
            if decision.decision is Decision.REQUIRE_AUTH:
                raise AuthorizationRequired(
                    "verified interactive authorization is required before execution"
                )
            if decision.decision is not Decision.ALLOW:
                raise GovernanceFailure(f"{named.name} returned an invalid decision")

        try:
            result = self._executor.execute(request)
        except Exception as exc:
            failure = BrokerDecision(
                Decision.DENY,
                "capability execution failed",
                request.request_id,
                "executor",
            )
            self._record(request, failure)
            raise ExecutionFailure("capability execution failed") from exc

        completed = BrokerDecision(
            Decision.ALLOW,
            "capability execution completed",
            request.request_id,
            "executor",
        )
        self._record(request, completed)
        return DispatchOutcome(request.request_id, DispatchStatus.EXECUTED, result=result)
