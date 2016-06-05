import math
import random


def to_seconds(milliseconds):
    """
    :func:`to_seconds` Converts :param:`milliseconds` to seconds.

    :param milliseconds: number of milliseconds you to convert to seconds
    :type milliseconds: float, int
    :return: seconds
    :rtype: float
    """
    return milliseconds / 1000.0


def to_ms(seconds):
    """
    :func:`to_ms` Converts :param:`seconds` to milliseconds.

    :param seconds: number of seconds you want to convert to milliseconds
    :type seconds: float, int
    :return: milliseconds
    :rtype: float
    """
    return seconds * 1000.0


class Backoff(object):

    def __init__(self, min_ms=100.0, max_ms=10000.0, factor=2.0, jitter=False):
        """
        :class:`Backoff` is a counter. It starts at :attr:`min_ms`.
        After every call to :meth:`duration` it is multiplied by
        :attr:`factor`.
        It is capped at :attr:`max_ms`. It returns to :attr:`min_ms` on every
        call to :meth:`reset`.

        :class:`Backoff` is not thread-safe, but the :meth:`for_attempt` method
        can be used concurrently if non-zero values for :attr:`factor`,
        :attr:`max_ms`, and :attr:`min_ms` are set on the :class:`Backoff`
        shared among threads.

        :param min_ms: min_ms is the minimum value of the counter
        :param max_ms: max_ms is the maximum value of the counter
        :param factor: factor is the multiplying factor for each increment step
        :param bool jitter: jitter eases contention by randomizing backoff
        steps
        :type min_ms: float, int
        :type max_ms: float, int
        :type factor: float, int
        :type jitter: bool
        """
        self.min_ms = float(min_ms)
        self.max_ms = float(max_ms)
        self.factor = float(factor)
        self.jitter = jitter

        self.cur_attempt = 0.0

    def duration(self):
        """
        Returns the current value of the counter and then multiplies it by
        :attr:`factor`

        :rtype: float
        """
        d = self.for_attempt(self.cur_attempt)
        self.cur_attempt += 1
        return d

    def for_attempt(self, attempt):
        """
        :meth:`for_attempt` returns the duration for a specific attempt.
        This is useful if you have a large number of independent backoffs,
        but don't want to use unnecessary memory storing the backoff parameters
        per backoff. The first attempt should be 0.
        :meth:`for_attempt` is thread-safe if non-zero values for
        :attr:`factor`, :attr:`max_ms`, and :attr:`min_ms` are set before
        any calls to :meth:`for_attempt` are made.

        :param attempt: the attempt you want to return duration for
        :type attempt: float
        :return: duration in seconds
        :rtype: float
        """
        dur = float(self.min_ms * math.pow(self.factor, attempt))

        if self.jitter:
            dur = random.random() * (dur - self.min_ms) + self.min_ms

        if dur > self.max_ms:
            return to_seconds(self.max_ms)

        return to_seconds(dur)

    def reset(self):
        """
        Resets the number of attempts to :attr:`min_ms`.
        """
        self.cur_attempt = round(to_seconds(self.min_ms))

    def attempt(self):
        """
        Returns the current backoff attempt.

        :rtype: float
        """
        return self.cur_attempt
