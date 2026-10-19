"""Canonical request, decision, and outcome models for the ODIN broker."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_AUTH = "require_auth"


class DispatchStatus(str, Enum):
    EXECUTED = "executed"
    DENIED = "denied"
    AUTH_REQUIRED = "auth_required"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class CommandEnvelope:
    actor: str
    capability: str
    action: str
    args: Mapping[str, Any] = field(default_factory=dict)
    risk: str = "unknown"
    project_id: str | None = None
    request_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        for name in ("actor", "capability", "action", "request_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        # Prevent a caller from mutating the top-level argument map after a gate approves it.
        object.__setattr__(self, "args", MappingProxyType(dict(self.args)))


@dataclass(frozen=True, slots=True)
class BrokerDecision:
    decision: Decision
    reason: str
    request_id: str
    gate: str = "unknown"


@dataclass(frozen=True, slots=True)
class DispatchOutcome:
    request_id: str
    status: DispatchStatus
    result: Any = None
    reason: str | None = None
