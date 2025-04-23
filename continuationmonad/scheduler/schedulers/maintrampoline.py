from abc import abstractmethod
from typing import Callable

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.utils.framesummary import get_frame_summary


class MainTrampoline(Trampoline):       # todo: delete
    @property
    @abstractmethod
    def is_stopped(self) -> bool: ...

    @is_stopped.setter
    @abstractmethod
    def is_stopped(self, val: bool): ...

    def stop(self):
        """
        The stop function is capable of creating the finishing Continuation
        """

        with self.lock:
            if self.is_stopped:
                raise Exception("Scheduler can only be stopped once.")
            self.is_stopped = True

        return self._create_certificate(weight=1, stack=get_frame_summary())

    def run(
        self,
        task: Callable[[], ContinuationCertificate],
        cancellation: Cancellation | None = None,
    ) -> None:
        super().run(
            task=task,
            cancellation=cancellation,
            weight=1,
        )
