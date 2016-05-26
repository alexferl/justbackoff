import math
import random


def to_seconds(milliseconds):
    return milliseconds / 1000


def to_ms(seconds):
    return seconds * 1000


class Backoff(object):

    def __init__(self, min=100.0, max=10000.0, factor=2.0, jitter=False):
        """
        :class:`Backoff` is a counter. It starts at :attr:`min`.
        After every call to :meth:`duration` it is multiplied by :attr:`factor`.
        It is capped at :attr:`max`. It returns to :attr:`min` on every call to :meth:`reset`.

        :class:`Backoff` is not thread-safe, but the :meth:`for_attempt` method can be
        used concurrently if non-zero values for :attr:`factor`, :attr:`max`, and :attr:`min`
        are set on the :class:`Backoff` shared among threads.

        :param min: min is the minimum value of the counter
        :param max: max is the maximum value of the counter
        :param factor: factor is the multiplying factor for each increment step
        :param bool jitter: jitter eases contention by randomizing backoff steps
        :type min: float, int
        :type max: float, int
        :type factor: float, int
        :type jitter: bool
        """
        self.min = float(min)
        self.max = float(max)
        self.factor = float(factor)
        self.jitter = jitter

        self.cur_attempt = 0.0

    def duration(self):
        """
        Returns the current value of the counter and then multiplies it by :attr:`factor`

        :rtype: float
        """
        d = self.for_attempt(self.cur_attempt)
        self.cur_attempt += 1
        return d

    def for_attempt(self, attempt):
        """
        :meth:`for_attempt` returns the duration for a specific attempt. This is useful if
        you have a large number of independent backoffs, but don't want use
        unnecessary memory storing the backoff parameters per backoff. The first
        attempt should be 0.
        :meth:`for_attempt` is thread-safe if non-zero values for :attr:`factor`, :attr:`max`, and :attr:`min`
        are set before any calls to :meth:`for_attempt` are made.

        :param attempt: the attempt you want to return duration for
        :type attempt: float
        :return: duration in milliseconds
        :rtype: float
        """
        dur = float(self.min * math.pow(self.factor, attempt))

        if self.jitter:
            dur = random.random() * (dur - self.min) + self.min

        if dur > self.max:
            return to_seconds(self.max)

        return to_seconds(dur)

    def reset(self):
        """
        Resets the number of attempts to :attr:`min`.
        """
        self.cur_attempt = round(to_seconds(self.min))

    def attempt(self):
        """
        Returns the current backoff attempt.

        :rtype: float
        """
        return self.cur_attempt
