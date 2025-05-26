from abc import abstractmethod
from threading import Lock
from typing import Callable

from continuationmonad.scheduler.instantscheduler import InstantScheduler
from continuationmonad.utils.framesummary import get_frame_summary
from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate


class MainSchedulerMixin(InstantScheduler):
    @property
    @abstractmethod
    def _weight(self) -> int: ...

    @_weight.setter
    @abstractmethod
    def _weight(self, val: int): ...

    @property
    @abstractmethod
    def lock(self) -> Lock: ...

    def stop(self, weight: int) -> ContinuationCertificate:
        with self.lock:
            n_weight = self._weight - weight
            self._weight = n_weight

        assert 0 <= n_weight, "Scheduler can only be stopped while weight is positive."

        return self._create_certificate(weight=weight, stack=get_frame_summary())

    # @abstractmethod
    def run(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None = None,
    ) -> None:
        # ...
        with self.lock:
            self._weight = weight

        self.schedule(task=task, weight=weight, cancellation=cancellation)