from typing import Callable, overload

from continuationmonad.cancellation import Cancellation
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.utils.framesummary import FrameSummary

class Scheduler:
    @overload
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
    ) -> ContinuationCertificate: ...
    @overload
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int | None,
    ) -> ContinuationCertificate: ...
    @overload
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        cancellation: Cancellation | None,
    ) -> ContinuationCertificate: ...
    @overload
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int | None,
        cancellation: Cancellation | None,
    ) -> ContinuationCertificate: ...
    def _create_certificates(
        self, 
        weight: int, 
        stack: tuple[FrameSummary, ...]
    ) -> ContinuationCertificate: ...
    def _execute_task(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ) -> None: ...
