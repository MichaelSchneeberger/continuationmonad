from abc import abstractmethod
import asyncio
import datetime
from typing import Callable, Coroutine, override

from continuationmonad.utils.framesummary import get_frame_summary
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.scheduler import Scheduler
from continuationmonad.scheduler.sequentialscheduler import SequentialScheduler
from continuationmonad.scheduler.mainschedulermixin import MainSchedulerMixin


class AsyncIOScheduler(SequentialScheduler, Scheduler):
    @property
    @abstractmethod
    def loop(
        self,
    ) -> asyncio.AbstractEventLoop: ...

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    @override
    def now(self):
        return datetime.datetime.now()

    @override
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ):
        # stack = get_frame_summary()

        def callback():
            self._execute_task(
                task=task,
                weight=weight,
                # stack=stack,
                cancellation=cancellation,
            )
        
        self.loop.call_soon_threadsafe(callback)

        certificate = self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )

        return certificate

    def schedule_asyncio(
        self,
        task: Coroutine,
        weight: int,
    ):
        async def coro():
            certificate = await task

            certificate.validate(weight=weight)

        asyncio_task = self.loop.create_task(coro())

        certificate = self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )

        return certificate, asyncio_task

    @override
    def schedule_relative(
        self,
        duetime: float,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ):
        def call_later():
            def callback():
                self._execute_task(
                    task=task,
                    weight=weight,
                    cancellation=cancellation,
                )

            self.loop.call_later(duetime, callback)

        self.loop.call_soon_threadsafe(call_later)

        certificate = self._create_certificate(
            weight=weight,
            stack=get_frame_summary(),
        )

        return certificate

    @override
    def schedule_absolute(
        self,
        duetime: datetime.datetime,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None,
    ):
        duetime_seconds = (duetime - self.now()).total_seconds()

        return self.schedule_relative(
            duetime=duetime_seconds,
            task=task,
            weight=weight,
            cancellation=cancellation,
        )


class MainAsyncIOScheduler(MainSchedulerMixin, AsyncIOScheduler):
    def stop(self, weight: int):
        """
        The stop function is capable of creating the finishing Continuation
        """

        def callback():
            self.loop.stop()

        self.loop.call_soon_threadsafe(callback)

        return super().stop(weight=weight)

    @override
    def run(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
        cancellation: Cancellation | None = None,
    ) -> None:
        super().run(task=task, weight=weight, cancellation=cancellation)
        # with self.lock:
        #     self._weight = weight

        # self.schedule(task=task, weight=1, cancellation=cancellation)

        self.start_loop()
