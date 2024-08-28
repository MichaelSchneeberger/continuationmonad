from __future__ import annotations

from collections import deque
from threading import RLock
from typing import Callable, override
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.scheduler import Scheduler


class Trampoline(Scheduler):
    def __init__(self):
        self.is_stopped = False
        self._queue = deque()
        self._lock = RLock()

    @property
    def lock(self) -> RLock:
        return self._lock

    @override
    def schedule(self, fn: Callable[[], Continuation]) -> Continuation:
        if self.is_stopped:
            raise Exception('Scheduler is stopped, no functions can be scheduled.')

        self._queue.append(fn)
        return self._create_continuation()

    def run(self, fn: Callable[[], Continuation]) -> Continuation:
        self._queue.append(fn)

        while self._queue:
            queued_fn = self._queue.popleft()

            # call scheduled function
            continuation = queued_fn()
            
            # verify that the continuation is used once
            continuation.verify()

        self.is_stopped = True
        return self._create_continuation()
