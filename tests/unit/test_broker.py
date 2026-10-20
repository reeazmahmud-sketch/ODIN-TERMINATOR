import pytest

from odin.core.broker import (
    AuditFailure,
    AuthorizationRequired,
    CapabilityBroker,
    ExecutionFailure,
    GovernanceFailure,
    RequestDenied,
)
from odin.core.models import BrokerDecision, CommandEnvelope, Decision, DispatchStatus


class Gate:
    def __init__(self, decision=Decision.ALLOW, *, fail=False, wrong_id=False):
        self.decision, self.fail, self.wrong_id = decision, fail, wrong_id

    def evaluate(self, request):
        if self.fail:
            raise RuntimeError("gate unavailable")
        request_id = "wrong" if self.wrong_id else request.request_id
        return BrokerDecision(self.decision, self.decision.value, request_id)


class Executor:
    def __init__(self, *, fail=False):
        self.called, self.fail = False, fail

    def execute(self, request):
        self.called = True
        if self.fail:
            raise RuntimeError("executor failed")
        return {"ok": True, "request_id": request.request_id}


class Audit:
    def __init__(self, *, fail=False):
        self.events, self.fail = [], fail

    def record(self, request, decision):
        if self.fail:
            raise RuntimeError("audit unavailable")
        self.events.append((decision.gate, request.request_id, decision.decision))


def make_broker(gates=None, executor=None, audit=None):
    gates = gates or [Gate() for _ in range(5)]
    return CapabilityBroker(
        identity=gates[0], project_guard=gates[1], policy=gates[2],
        risk=gates[3], authorization=gates[4],
        executor=executor or Executor(), audit=audit or Audit(),
    )


def request():
    return CommandEnvelope(actor="terminator", capability="files", action="read")


def test_all_gates_allow_then_execute():
    executor, audit = Executor(), Audit()
    outcome = make_broker(executor=executor, audit=audit).dispatch(request())
    assert outcome.status is DispatchStatus.EXECUTED
    assert executor.called is True
    assert [event[0] for event in audit.events] == [
        "identity", "project_guard", "policy", "risk", "authorization", "executor"
    ]


def test_denial_prevents_execution():
    executor = Executor()
    gates = [Gate(), Gate(), Gate(Decision.DENY), Gate(), Gate()]
    with pytest.raises(RequestDenied):
        make_broker(gates, executor).dispatch(request())
    assert executor.called is False


def test_auth_required_never_executes():
    executor = Executor()
    gates = [Gate(), Gate(), Gate(), Gate(), Gate(Decision.REQUIRE_AUTH)]
    with pytest.raises(AuthorizationRequired):
        make_broker(gates, executor).dispatch(request())
    assert executor.called is False


def test_gate_exception_fails_closed():
    executor = Executor()
    gates = [Gate(), Gate(fail=True), Gate(), Gate(), Gate()]
    with pytest.raises(GovernanceFailure):
        make_broker(gates, executor).dispatch(request())
    assert executor.called is False


def test_mismatched_request_id_fails_closed():
    executor = Executor()
    gates = [Gate(wrong_id=True), Gate(), Gate(), Gate(), Gate()]
    with pytest.raises(GovernanceFailure):
        make_broker(gates, executor).dispatch(request())
    assert executor.called is False


def test_audit_failure_blocks_execution():
    executor = Executor()
    with pytest.raises(AuditFailure):
        make_broker(executor=executor, audit=Audit(fail=True)).dispatch(request())
    assert executor.called is False


def test_executor_failure_is_audited_and_raised():
    audit = Audit()
    with pytest.raises(ExecutionFailure):
        make_broker(executor=Executor(fail=True), audit=audit).dispatch(request())
    assert audit.events[-1][0] == "executor"
    assert audit.events[-1][2] is Decision.DENY


def test_invalid_envelope_rejected():
    with pytest.raises(ValueError):
        CommandEnvelope(actor="", capability="files", action="read")
