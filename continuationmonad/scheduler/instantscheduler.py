from abc import ABC, abstractmethod
from threading import Lock
from typing import Callable

from continuationmonad.utils.framesummary import FrameSummary
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate, ContinuationCertificateMixin
from continuationmonad.scheduler.cancellation import Cancellation


class InstantScheduler(ABC):
    @abstractmethod
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None = None,
    ) -> ContinuationCertificate: ...

    def _execute_task(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        # stack: tuple[FrameSummary, ...],
        cancellation: Cancellation | None = None,
    ):
        # if task it cancelled, retrieve certificate from is_cancelled
        if cancellation and (certificate := cancellation.is_cancelled()):
            pass

        else:
            # call scheduled task
            certificate = task()

            if not isinstance(certificate, ContinuationCertificateMixin):
                raise AssertionError(f'Task {task} returned non valid certificate {certificate}.')

        certificate.validate(weight)

    def _create_certificate(
        self,
        weight: int,
        stack: tuple[FrameSummary, ...],
    ):
        # _ContinuationCertificate = type(
        #     ContinuationCertificate.__name__,
        #     ContinuationCertificate.__mro__,
        #     ContinuationCertificate.__dict__ | {"__permission__": True},
        # )
        return ContinuationCertificate(
            lock=Lock(), 
            weight=weight,
            stack=stack,
            validated=False,
        )
