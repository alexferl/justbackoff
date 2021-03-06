import unittest

from justbackoff import Backoff, to_ms, to_seconds


class CustomAssertions:
    @staticmethod
    def assert_between(actual: float, low: float, high: float):
        if actual < low:
            raise AssertionError("Got {}, expecting >= {}".format(actual, low))

        if actual > high:
            msg = "Got {}, expecting <= {}".format(actual, high)
            raise AssertionError(msg)


class TestBackoff(unittest.TestCase, CustomAssertions):
    def setUp(self):
        self.b = Backoff(min_ms=100.0, max_ms=10000.0, factor=2.0)

    def test_defaults(self):
        self.assertEqual(self.b.duration(), to_seconds(100.0))
        self.assertEqual(self.b.duration(), to_seconds(200.0))
        self.assertEqual(self.b.duration(), to_seconds(400.0))
        self.b.reset()
        self.assertEqual(self.b.duration(), to_seconds(100.0))

    def test_factor(self):
        b = Backoff(min_ms=100, max_ms=10000, factor=1.5)

        self.assertEqual(b.duration(), to_seconds(100.0))
        self.assertEqual(b.duration(), to_seconds(150.0))
        self.assertEqual(b.duration(), to_seconds(225.0))
        b.reset()
        self.assertEqual(b.duration(), to_seconds(100.0))

    def test_for_attempt(self):
        self.assertEqual(self.b.for_attempt(0), to_seconds(100.0))
        self.assertEqual(self.b.for_attempt(1), to_seconds(200.0))
        self.assertEqual(self.b.for_attempt(2), to_seconds(400.0))
        self.b.reset()
        self.assertEqual(self.b.for_attempt(0), to_seconds(100.0))

    def test_get_attempt(self):
        self.assertEqual(self.b.attempt(), 0)
        self.assertEqual(self.b.duration(), to_seconds(100.0))
        self.assertEqual(self.b.attempt(), 1)
        self.assertEqual(self.b.duration(), to_seconds(200.0))
        self.assertEqual(self.b.attempt(), 2)
        self.assertEqual(self.b.duration(), to_seconds(400.0))
        self.assertEqual(self.b.attempt(), 3)
        self.b.reset()
        self.assertEqual(self.b.attempt(), 0)
        self.assertEqual(self.b.duration(), to_seconds(100.0))
        self.assertEqual(self.b.attempt(), 1)

    def test_jitter(self):
        b = Backoff(min_ms=100.0, max_ms=10000.0, factor=2.0, jitter=True)

        self.assertEqual(b.duration(), to_seconds(100.0))
        self.assert_between(b.duration(), to_seconds(100.0), to_seconds(200.0))
        self.assert_between(b.duration(), to_seconds(100.0), to_seconds(400.0))
        b.reset()
        self.assertEqual(b.duration(), to_seconds(100.0))

    def test_integers(self):
        b = Backoff(min_ms=100, max_ms=10000, factor=2)

        self.assertEqual(b.duration(), to_seconds(100.0))
        self.assertEqual(b.duration(), to_seconds(200.0))
        self.assertEqual(b.duration(), to_seconds(400.0))
        b.reset()
        self.assertEqual(b.duration(), to_seconds(100.0))

    def test_to_ms(self):
        self.assertEqual(10000, to_ms(10.0))

    def test_min_bigger_than_max(self):
        b = Backoff(min_ms=10000.0, max_ms=1000.0, factor=2)

        self.assertEqual(b.duration(), 1.0)
        self.assertEqual(b.duration(), 1.0)
        self.assertEqual(b.duration(), 1.0)
        b.reset()
        self.assertEqual(b.duration(), 1.0)
