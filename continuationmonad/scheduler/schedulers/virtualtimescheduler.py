from abc import abstractmethod
import datetime
import heapq
from threading import Lock
from typing import Callable, Deque, override

from continuationmonad.utils.framesummary import get_frame_summary
from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.mainschedulermixin import MainSchedulerMixin
from continuationmonad.scheduler.scheduledtask import VirtualScheduledTask, ScheduledTask
from continuationmonad.scheduler.scheduler import Scheduler
from continuationmonad.scheduler.sequentialscheduler import SequentialScheduler


class VirtualTimeScheduler(SequentialScheduler, Scheduler):
    @property
    @abstractmethod
    def immediate_tasks(
        self,
    ) -> Deque[ScheduledTask]: ...

    @property
    @abstractmethod
    def delayed_tasks(
        self,
    ) -> list[VirtualScheduledTask]: ...

    @property
    @abstractmethod
    def lock(self) -> Lock: ...

    @property
    @abstractmethod
    def delayed_task_lock(self) -> Lock: ...

    @property
    @abstractmethod
    def start_datetime(self) -> datetime.datetime: ...

    @property
    @abstractmethod
    def _time(self) -> float: ...

    @_time.setter
    @abstractmethod
    def _time(self, val: float): ...

    @property
    @abstractmethod
    def _idle(self) -> bool: ...

    @_idle.setter
    @abstractmethod
    def _idle(selfc, val: bool): ...

    @override
    def now(self):
        return self.start_datetime + datetime.timedelta(seconds=self._time)

    @override
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ):
        entry = ScheduledTask(
            task=task,
            weight=weight,
            cancellation=cancellation,
            stack=get_frame_summary()
        )

        self.immediate_tasks.append(entry)

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
        cancellation: Cancellation | None,
    ):
        entry = VirtualScheduledTask(
            duetime=self._time + duetime,
            task=task,
            weight=weight,
            cancellation=cancellation,
            stack=get_frame_summary()
        )

        with self.delayed_task_lock:
            heapq.heappush(self.delayed_tasks, entry)

        return self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )

    @override
    def schedule_absolute(
        self,
        duetime: datetime.datetime,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ):
        duetime_time = (duetime - self.start_datetime).total_seconds()

        return self.schedule_relative(
            duetime=duetime_time,
            task=task,
            weight=weight,
            cancellation=cancellation,
        )

    def advance_to(self, time: float):
        with self.lock:
            idle = self._idle
            self._idle = False

        assert idle

        while True:
            if self.immediate_tasks:
                entry = self.immediate_tasks.popleft()

                self._execute_task(
                    task=entry.task,
                    weight=entry.weight,
                    cancellation=entry.cancellation,
                )

            elif self.delayed_tasks:
                schedule_due = False
                entry = None

                with self.delayed_task_lock:
                    entry = self.delayed_tasks[0]
                    if entry.duetime <= self._time:
                        entry = heapq.heappop(self.delayed_tasks)
                        schedule_due = True


                if schedule_due:
                    self.immediate_tasks.append(entry)

                elif entry.duetime <= time:
                    self._time = entry.duetime
                    
                else:
                    self._idle = True
                    break

            else:
                with self.lock:
                    if self.immediate_tasks or self.delayed_tasks:
                        pass

                    else:
                        self._idle = True
                        break


class MainVirtualTimeScheduler(MainSchedulerMixin, VirtualTimeScheduler):
    # @property
    # @abstractmethod
    # def is_stopped(self) -> bool: ...

    # @is_stopped.setter
    # @abstractmethod
    # def is_stopped(selfc, val: bool): ...

    # def stop(self, weight: int):
    #     """
    #     The stop function is capable of creating the finishing Continuation
    #     """

    #     with self.lock:
    #         if self.is_stopped:
    #             raise Exception("Scheduler can only be stopped once.")
    #         self.is_stopped = True

    #     return super().stop(weight=weight)
    
    # @override
    # def run(
    #     self,
    #     task: Callable[[], ContinuationCertificate],
    #     weight: int,
    #     cancellation: Cancellation | None = None,
    # ) -> None:
        
    #     super().run(task=task, weight=weight, cancellation=cancellation)

        # with self.lock:
        #     self._weight = weight

        # #     if not self.is_stopped:
        # #         raise Exception("Scheduler can only be run once.")
        # #     self.is_stopped = False
        
        # self.schedule(task=task, weight=self._weight, cancellation=cancellation)
    pass