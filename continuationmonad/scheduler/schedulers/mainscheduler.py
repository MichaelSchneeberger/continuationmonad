from abc import abstractmethod
from typing import Callable

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.schedulers.eventloopscheduler import EventLoopScheduler
from continuationmonad.utils.framesummary import get_frame_summary


class MainScheduler(EventLoopScheduler):
    def stop(self):
        """
        The stop function is capable of creating the finishing Continuation
        """

        with self.lock:
            if self.is_stopped:
                raise Exception("Scheduler can only be stopped once.")
            self.is_stopped = True

            self.condition.notify()

        return self._create_certificate(weight=1, stack=get_frame_summary())

    def run(
        self,
        task: Callable[[], ContinuationCertificate],
        cancellation: Cancellation | None = None,
    ) -> None:
        
        self.schedule(task=task, weight=1, cancellation=cancellation)

        self.start_loop()
