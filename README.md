# justbackoff

[![Build Status](https://travis-ci.org/admiralobvious/justbackoff.svg?branch=master)](https://travis-ci.org/admiralobvious/justbackoff)

A simple backoff algorithm for Python >3.6.


### Install

```shell script
$ pip install justbackoff
```

### Usage

Backoff is a counter. It starts at `min_ms`. After every call to `duration()`,
it is multiplied by `factor`. It is capped at `max_ms`.
It returns to `min_ms` on every call to `reset()`.
`jitter` adds randomness ([see below](#example-using-jitter)).

---

#### Simple example

``` python
from justbackoff import Backoff

b = Backoff(min_ms=100, max_ms=10000, factor=2, jitter=False)

print(b.duration())
print(b.duration())
print(b.duration())

print("Reset!")
b.reset()

print(b.duration())

```

``` shell script
0.1
0.2
0.4
Reset!
0.1
```

---

#### Example using `socket` package

``` python
import socket
import time

from justbackoff import Backoff


sock = socket.socket()
b = Backoff()

while True:
    try:
        sock.connect(("127.0.0.1", 1337))
    except Exception as e:
        d = b.duration()
        print("{}, reconnecting in {} seconds".format(e, d))
        time.sleep(d)
        continue

    b.reset()
    sock.send("Hello, world!")
    sock.close()

```

---

#### Example using `jitter`

Enabling `jitter` adds some randomization to the backoff durations.
[See Amazon's writeup of performance gains using jitter](http://www.awsarchitectureblog.com/2015/03/backoff.html).
Seeding is not necessary but doing so gives repeatable results.

```python
import random

from justbackoff import Backoff

b = Backoff(min_ms=100, max_ms=10000, factor=2, jitter=True)

random.seed(42)

print(b.duration())
print(b.duration())
print(b.duration())

print("Reset!")
b.reset()

print(b.duration())
print(b.duration())
print(b.duration())
```

``` shell script
0.1
0.102501075522
0.182508795511
Reset!
0.1
0.173647121416
0.303009846227
```

#### Credits

Ported from Go [backoff](https://github.com/jpillora/backoff)
