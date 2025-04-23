from abc import abstractmethod

from typing import Callable

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.instantscheduler import InstantScheduler


class Scheduler(InstantScheduler):
    @abstractmethod
    def schedule_relative(
        self,
        duetime: float,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None = None,
    ) -> ContinuationCertificate: ...
