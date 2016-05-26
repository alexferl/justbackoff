# justbackoff

A simple backoff algorithm in Python


### Install

```
$ pip install justbackoff
```

### Usage

Backoff is a counter. It starts at `min`. After every call to `duration()` it is multiplied by `factor`. It is capped at `max`. It returns to `min` on every call to `reset()`. `jitter` adds randomness ([see below](#example-using-jitter)).

---

#### Simple example

``` python
from justbackoff import Backoff, to_ms

b = Backoff(min=100, max=10000, factor=2, jitter=False)

print(b.duration())
print(b.duration())
print(b.duration())

print("Reset!")
b.reset()

print(b.duration())

```

```
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

Enabling `jitter` adds some randomization to the backoff durations. [See Amazon's writeup of performance gains using jitter](http://www.awsarchitectureblog.com/2015/03/backoff.html). Seeding is not necessary but doing so gives repeatable results.

```python
import random

from justbackoff import Backoff, to_ms

b = Backoff(min=100, max=10000, factor=2, jitter=True)

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

```
0.1
0.102501075522
0.182508795511
Reset!
0.1
0.173647121416
0.303009846227
```

#### Credits

Ported from Go (golang) [backoff](https://github.com/jpillora/backoff)
