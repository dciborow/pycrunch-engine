from uuid import uuid4


class TestRunPlan():
    def __init__(self, tests, id=None):
        self.id = id or str(uuid4())
        self.tests = tests
