from __future__ import annotations

from collections import deque
from threading import RLock
from typing import Callable, Deque, override

from continuationmonad.cancellation import Cancellation
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.utils.framesummary import get_frame_summary


class Trampoline(Scheduler):
    def __init__(self):
        self.is_stopped = False
        self._queue: Deque[
            tuple[
                Callable[[], ContinuationCertificate],
                int,
                Cancellation | None,
            ]
        ] = deque()
        self._lock = RLock()

    @property
    def lock(self) -> RLock:
        return self._lock

    def run(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int | None = None,
        cancellation: Cancellation | None = None,
    ):
        first_certificate = self.schedule(task=task, weight=weight, cancellation=cancellation)

        while self._queue:
            queued_task, queued_weight, queued_cancel_task = self._queue.popleft()

            self._execute_task(
                task=queued_task,
                weight=queued_weight,
                cancellation=queued_cancel_task,
            )

        return first_certificate

    @override
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int | None = None,
        cancellation: Cancellation | None = None,
    ):
        if weight is None:
            weight = 1

        self._queue.append((task, weight, cancellation))
        return self._create_certificates(
            weight=weight,
            stack=get_frame_summary(),
        )
