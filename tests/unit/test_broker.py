from odin.core.broker import CapabilityBroker
from odin.core.models import BrokerDecision, CommandEnvelope, Decision


class Gate:
    def __init__(self, decision: Decision = Decision.ALLOW):
        self.decision = decision

    def evaluate(self, request):
        return BrokerDecision(self.decision, self.decision.value, request.request_id)


class Executor:
    def __init__(self):
        self.called = False

    def execute(self, request):
        self.called = True
        return {"ok": True, "request_id": request.request_id}


class Audit:
    def __init__(self):
        self.events = []

    def record(self, request, decision):
        self.events.append((request.request_id, decision.decision))


def make_broker(gates, executor, audit):
    return CapabilityBroker(
        identity=gates[0], project_guard=gates[1], policy=gates[2],
        risk=gates[3], authorization=gates[4], executor=executor, audit=audit
    )


def test_all_gates_must_allow_before_execution():
    executor, audit = Executor(), Audit()
    broker = make_broker([Gate() for _ in range(5)], executor, audit)
    result = broker.dispatch(CommandEnvelope(actor="terminator", capability="files", action="read"))
    assert result["ok"] is True
    assert executor.called is True


def test_denial_prevents_execution():
    executor, audit = Executor(), Audit()
    gates = [Gate(), Gate(), Gate(Decision.DENY), Gate(), Gate()]
    broker = make_broker(gates, executor, audit)
    try:
        broker.dispatch(CommandEnvelope(actor="agent", capability="files", action="delete"))
    except PermissionError:
        pass
    else:
        raise AssertionError("denied request executed")
    assert executor.called is False


def test_auth_required_does_not_execute():
    executor, audit = Executor(), Audit()
    gates = [Gate(), Gate(), Gate(), Gate(), Gate(Decision.REQUIRE_AUTH)]
    broker = make_broker(gates, executor, audit)
    try:
        broker.dispatch(CommandEnvelope(actor="terminator", capability="macos", action="privileged"))
    except PermissionError:
        pass
    else:
        raise AssertionError("authorization-required request executed")
    assert executor.called is False
