from abc import ABC, abstractmethod
from threading import RLock
from typing import Callable

from continuationmonad.exceptions import ContinuationMonadSchedulerException
from continuationmonad.cancellation import Cancellation
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.utils.framesummary import FrameSummary


class Scheduler(ABC):
    @property
    @abstractmethod
    def lock(self) -> RLock: ...

    @abstractmethod
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int | None = None,
        cancellation: Cancellation | None = None,
    ) -> ContinuationCertificate: ...

    def _execute_task(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None = None,
    ):
        # if task it cancelled, retrieve certificate from is_cancelled
        if cancellation and (
            certificate := cancellation.is_cancelled()
        ):
            pass

        else:
            # call scheduled task
            certificate = task()

        certificate.verify(weight=weight)
    def _create_certificates(
        self,
        weight: int,
        stack: tuple[FrameSummary, ...],
    ):
        _ContinuationCertificate = type(
            ContinuationCertificate.__name__,
            ContinuationCertificate.__mro__,
            ContinuationCertificate.__dict__ | {"__permission__": True},
        )
        return _ContinuationCertificate(lock=self.lock, weight=weight, stack=stack)
