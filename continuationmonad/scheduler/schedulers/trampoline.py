from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Deque, override

from continuationmonad.scheduler.sequentialscheduler import SequentialScheduler
from continuationmonad.utils.framesummary import FrameSummary, get_frame_summary
from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.instantscheduler import InstantScheduler
from continuationmonad.scheduler.mainschedulermixin import MainSchedulerMixin


class Trampoline(SequentialScheduler, InstantScheduler):
    @property
    @abstractmethod
    def queue(self) -> Deque[
        tuple[
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...]
        ]
    ]: ...

    @property
    @abstractmethod
    def is_running(self) -> bool: ...

    @is_running.setter
    @abstractmethod
    def is_running(self, val: bool): ...
    
    def start_loop(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ):
        self.is_running = True

        first_certificate = self.schedule(task=task, weight=weight, cancellation=cancellation)

        while self.queue:
            queued_task, queued_weight, queued_cancel_task, stack = self.queue.popleft()

            self._execute_task(
                task=queued_task,
                weight=queued_weight,
                # stack=stack,
                cancellation=queued_cancel_task,
            )

        self.is_running = False

        return first_certificate

    @override
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ):
        assert self.is_running

        stack = get_frame_summary()

        self.queue.append((task, weight, cancellation, stack))

        return self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )


class MainTrampoline(Trampoline, MainSchedulerMixin):
    @override
    def run(
        self,
        task: Callable[[], ContinuationCertificate],
        # weight: int,
        cancellation: Cancellation | None = None,
    ):
        super().start_loop(task=task, cancellation=cancellation, weight=1)
