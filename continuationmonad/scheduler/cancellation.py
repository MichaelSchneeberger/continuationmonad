from abc import ABC, abstractmethod

from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate


class Cancellation(ABC):
    """Used to cancel a task scheduled on a scheduler."""

    @abstractmethod
    def is_cancelled(
        self,
    ) -> (
        ContinuationCertificate | None
    ): ...


# class Cancellable(ABC):
#     """Used to cancel a task scheduled on a scheduler."""

#     @abstractmethod
#     def cancel(self, certificate: ContinuationCertificate) -> None:
#         ...
