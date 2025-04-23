from abc import abstractmethod
from threading import Condition, Lock
from typing import Callable, Deque, override
import datetime

from continuationmonad.utils.framesummary import FrameSummary, get_frame_summary
from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.scheduler import Scheduler


class EventLoopScheduler(Scheduler):
    @property
    @abstractmethod
    def immediate_tasks(
        self,
    ) -> Deque[
        tuple[
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]: ...

    @property
    @abstractmethod
    def delayed_tasks(
        self,
    ) -> list[
        tuple[
            datetime.datetime,
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]: ...

    @property
    @abstractmethod
    def lock(self) -> Lock: ...

    @property
    @abstractmethod
    def delayed_task_lock(self) -> Lock: ...

    @property
    @abstractmethod
    def condition(self) -> Condition: ...

    @property
    @abstractmethod
    def is_stopped(self) -> bool: ...

    @is_stopped.setter
    @abstractmethod
    def is_stopped(self, val: bool): ...

    def start_loop(self):
        while True:
            if self.is_stopped:
                break

            elif self.immediate_tasks:
                task, weight, cancellation, stack = (
                    self.immediate_tasks.popleft()
                )

                self._execute_task(
                    task=task,
                    weight=weight,
                    stack=stack,
                    cancellation=cancellation,
                )

            elif self.delayed_tasks:
                scheduled_time, task, weight, cancellation, stack = self.delayed_tasks[0]

                timedelta = datetime.datetime.now() - scheduled_time

                if datetime.timedelta(0) < timedelta:
                    self.delayed_tasks.pop(0)
                    self.immediate_tasks.append((task, weight, cancellation, stack))

                else:
                    with self.lock:
                        self.condition.wait(timedelta.total_seconds())

            else:
                with self.lock:
                    if self.immediate_tasks or self.delayed_tasks or self.is_stopped:
                        pass
                    
                    else:
                        self.condition.wait()

    @override
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None = None,
    ):
        stack = get_frame_summary()

        self.immediate_tasks.append((task, weight, cancellation, stack))

        with self.lock:
            self.condition.notify()

        return self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )

    @override
    def schedule_relative(
        self,
        duetime: float,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None = None,
    ):
        stack = get_frame_summary()

        duetime_datetime = datetime.datetime.now() + datetime.timedelta(duetime)

        entry = duetime_datetime, task, weight, cancellation, stack

        with self.delayed_task_lock:
            for idx, (d, *_) in enumerate(self.delayed_tasks):
                if duetime_datetime <= d:
                    self.delayed_tasks.insert(idx, entry)
                    break
            else:
                self.delayed_tasks.append(entry)

        with self.lock:
            self.condition.notify()

        return self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )
