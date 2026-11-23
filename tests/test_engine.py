import pytest
from consumer.models import WidgetRequest
from consumer.engine import Engine



class MockReceiver:
    def __init__(self, requests):
        self.requests = list(requests)

    def get_next_request(self):
        if self.requests:
            return self.requests.pop(0)
        else:
            return None

class MockStorage:
    def __init__(self):
        self.stored = []

    def store(self, widget):
        self.stored.append(widget)

    def update(self, widget):
        self.stored.append(widget)

    def delete(self, widget):
        self.stored.append(widget)


def test_engine_processes_create():
    req = WidgetRequest(request_id=1, widget_type="create", widget_id=1, owner="test", label="test")
    receiver = MockReceiver([req])
    storage = MockStorage()

    engine = Engine(receiver=receiver, storage=storage, max_iterations=1)
    engine.run()

    assert storage.stored[0] == req

def test_engine_processes_update():
    req = WidgetRequest(request_id=1, widget_type="update", widget_id=1, owner="test", label="test")
    receiver = MockReceiver([req])
    storage = MockStorage()

    engine = Engine(receiver=receiver, storage=storage, max_iterations=1)
    engine.run()

    assert storage.stored[0] == req

def test_engine_processes_delete():
    req = WidgetRequest(request_id=1, widget_type="delete", widget_id=1, owner="test", label="test")
    receiver = MockReceiver([req])
    storage = MockStorage()

    engine = Engine(receiver=receiver, storage=storage, max_iterations=1)
    engine.run()

    assert storage.stored[0] == req