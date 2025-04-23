from __future__ import annotations

from collections import deque
from threading import Condition, Lock, Thread
from typing import Callable, Deque
import datetime

from dataclassabc import dataclassabc

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.currentthreadscheduler import (
    CurrentThreadScheduler,
)
from continuationmonad.scheduler.schedulers.eventloopscheduler import (
    EventLoopScheduler,
)
from continuationmonad.scheduler.schedulers.mainscheduler import MainScheduler
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.utils.framesummary import FrameSummary


# def init_main_trampoline():
#     return MainTrampoline()


@dataclassabc
class CurrentThreadSchedulerImpl(CurrentThreadScheduler):
    immediate_tasks: Deque[
        tuple[
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]
    delayed_tasks: list[
        tuple[
            datetime.datetime,
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]
    lock: Lock
    delayed_task_lock: Lock
    condition: Condition
    idle: bool


def init_current_thread_scheduler():
    lock = Lock()
    delayed_task_lock = Lock()

    return CurrentThreadSchedulerImpl(
        immediate_tasks=deque(),
        delayed_tasks=[],
        lock=lock,
        delayed_task_lock=delayed_task_lock,
        condition=Condition(lock),
        idle=True,
    )


@dataclassabc(frozen=True)
class EventLoopSchedulerImpl(EventLoopScheduler):
    immediate_tasks: Deque[
        tuple[
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]
    delayed_tasks: list[
        tuple[
            datetime.datetime,
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]
    lock: Lock
    delayed_task_lock: Lock
    condition: Condition
    is_stopped: bool


def init_event_loop_scheduler():
    lock = Lock()
    delayed_task_lock = Lock()

    scheduler = EventLoopSchedulerImpl(
        immediate_tasks=deque(),
        delayed_tasks=[],
        lock=lock,
        delayed_task_lock=delayed_task_lock,
        condition=Condition(lock),
        is_stopped=False,
    )

    Thread(target=scheduler.start_loop, daemon=True).start()

    return scheduler


@dataclassabc
class MainSchedulerImpl(MainScheduler):
    immediate_tasks: Deque[
        tuple[
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]
    delayed_tasks: list[
        tuple[
            datetime.datetime,
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]
    lock: Lock
    delayed_task_lock: Lock
    condition: Condition
    is_stopped: bool


def init_main_scheduler():
    lock = Lock()
    delayed_task_lock = Lock()

    return MainSchedulerImpl(
        immediate_tasks=deque(),
        delayed_tasks=[],
        lock=lock,
        delayed_task_lock=delayed_task_lock,
        condition=Condition(lock),
        is_stopped=False,
    )


@dataclassabc(frozen=True)
class TrampolineImpl(Trampoline):
    queue: Deque[
        tuple[
            Callable[[], ContinuationCertificate],
            int,
            Cancellation | None,
            tuple[FrameSummary, ...],
        ]
    ]


def init_trampoline():
    return TrampolineImpl(
        queue=deque(),
    )
