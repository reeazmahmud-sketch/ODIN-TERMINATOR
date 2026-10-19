"""Canonical request/decision models for the ODIN Capability Broker."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_AUTH = "require_auth"


@dataclass(frozen=True, slots=True)
class CommandEnvelope:
    actor: str
    capability: str
    action: str
    args: dict[str, Any] = field(default_factory=dict)
    risk: str = "unknown"
    project_id: str | None = None
    intent_hash: str | None = None
    request_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True, slots=True)
class BrokerDecision:
    decision: Decision
    reason: str
    request_id: str
