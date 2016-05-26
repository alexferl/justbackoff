import unittest

from justbackoff import Backoff, to_seconds


class CustomAssertions(object):

    def assertBetween(self, actual, low, high):
        if actual < low:
            raise AssertionError('Got {}, expecting >= {}'.format(actual, low))

        if actual > high:
            raise AssertionError('Got {}, expecting <= {}'.format(actual, high))

"""
func TestGetAttempt(t *testing.T) {
	b := &Backoff{
		Min:    100 * time.Millisecond,
		Max:    10 * time.Second,
		Factor: 2,
	}
	equals(t, b.Attempt(), float64(0))
	equals(t, b.Duration(), 100*time.Millisecond)
	equals(t, b.Attempt(), float64(1))
	equals(t, b.Duration(), 200*time.Millisecond)
	equals(t, b.Attempt(), float64(2))
	equals(t, b.Duration(), 400*time.Millisecond)
	equals(t, b.Attempt(), float64(3))
	b.Reset()
	equals(t, b.Attempt(), float64(0))
	equals(t, b.Duration(), 100*time.Millisecond)
	equals(t, b.Attempt(), float64(1))
"""

class TestBackoff(unittest.TestCase, CustomAssertions):

    def setUp(self):
        self.b = Backoff(min=100.0, max=10000.0, factor=2.0)

    def test_defaults(self):
        self.assertEqual(self.b.duration(), to_seconds(100.0))
        self.assertEqual(self.b.duration(), to_seconds(200.0))
        self.assertEqual(self.b.duration(), to_seconds(400.0))
        self.b.reset()
        self.assertEqual(self.b.duration(), to_seconds(100.0))

    def test_factor(self):
        b = Backoff(min=100, max=10000, factor=1.5)

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
        b = Backoff(min=100.0, max=10000.0, factor=2.0, jitter=True)

        self.assertEqual(b.duration(), to_seconds(100.0))
        self.assertBetween(b.duration(), to_seconds(100.0), to_seconds(200.0))
        self.assertBetween(b.duration(), to_seconds(100.0), to_seconds(400.0))
        b.reset()
        self.assertEqual(b.duration(), to_seconds(100.0))

    def test_integers(self):
        b = Backoff(min=100, max=10000, factor=2)

        self.assertEqual(b.duration(), to_seconds(100.0))
        self.assertEqual(b.duration(), to_seconds(200.0))
        self.assertEqual(b.duration(), to_seconds(400.0))
        b.reset()
        self.assertEqual(b.duration(), to_seconds(100.0))
