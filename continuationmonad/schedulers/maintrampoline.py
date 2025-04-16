from typing import Callable
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.utils.framesummary import get_frame_summary


class MainTrampoline(Trampoline):
    def __init__(self):
        self.is_stopped = False

        super().__init__()

    def stop(self):
        """
        The stop function is capable of creating the finishing Continuation
        """

        with self._lock:
            if self.is_stopped:
                raise Exception("Scheduler can only be stopped once.")
            self.is_stopped = True

        return self._create_certificates(weight=1, stack=get_frame_summary())

    def run(
        self,
        task: Callable[[], ContinuationCertificate],
    ) -> None:
        super().run(
            task=task,
        )
