from abc import abstractmethod
from threading import Condition, Lock
from typing import Callable, Deque, override
import datetime

from continuationmonad.utils.framesummary import FrameSummary, get_frame_summary
from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.scheduler import Scheduler


class CurrentThreadScheduler(Scheduler):
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
    def idle(self) -> bool: ...

    @idle.setter
    @abstractmethod
    def idle(selfc, val: bool): ...

    def _start_loop(self):
        while True:
            if self.immediate_tasks:
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

                schedule_due = False
                entry = None

                with self.delayed_task_lock:
                    entry = self.delayed_tasks[0]
                    if datetime.timedelta(0) < datetime.datetime.now() - entry[0]:
                        entry = self.delayed_tasks.pop(0)
                        schedule_due = True


                if schedule_due:
                    self.immediate_tasks.append(entry)

                else:
                    timedelta = datetime.datetime.now() - entry[0]
                    self.condition.wait(timedelta.total_seconds())

            else:
                with self.lock:
                    if self.immediate_tasks or self.delayed_tasks:
                        pass

                    else:
                        self.idle = True
                        break

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
            idle = self.idle
            self.idle = False

            self.condition.notify()

        if idle:
            self._start_loop()

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
            idle = self.idle
            self.idle = False

            self.condition.notify()

        if idle:
            self._start_loop()

        return self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )
