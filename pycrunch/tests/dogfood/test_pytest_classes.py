import unittest


class MyClass(unittest.TestCase):
    def test_method1(self):
        assert True

    def test_method2(self):
        assert True


class TestForDummies(unittest.TestCase):
    def test_method1(self):
        assert True

    def test_method2(self):
        assert True

    def helper_method(self):
        # should not be in tests
        pass