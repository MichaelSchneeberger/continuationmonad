from __future__ import annotations

import asyncio
from collections import deque
import datetime
from threading import Condition, Lock, Thread
from typing import Deque

from dataclassabc import dataclassabc

from continuationmonad.scheduler.scheduledtask import DelayedScheduledTask, ScheduledTask, VirtualScheduledTask
from continuationmonad.scheduler.schedulers.asyncioscheduler import AsyncIOScheduler, MainAsyncIOScheduler
from continuationmonad.scheduler.schedulers.currentthreadscheduler import (
    CurrentThreadScheduler,
)
from continuationmonad.scheduler.schedulers.eventloopscheduler import (
    EventLoopScheduler,
    MainScheduler,
)
from continuationmonad.scheduler.schedulers.trampoline import MainTrampoline, Trampoline
from continuationmonad.scheduler.schedulers.virtualtimescheduler import MainVirtualTimeScheduler, VirtualTimeScheduler


# def init_main_trampoline():
#     return MainTrampoline()


@dataclassabc
class CurrentThreadSchedulerImpl(CurrentThreadScheduler):
    immediate_tasks: Deque[ScheduledTask]
    delayed_tasks: list[DelayedScheduledTask]
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


@dataclassabc(frozen=False)
class EventLoopSchedulerImpl(EventLoopScheduler):
    immediate_tasks: Deque[ScheduledTask]
    delayed_tasks: list[DelayedScheduledTask]
    lock: Lock
    delayed_task_lock: Lock
    condition: Condition
    _is_stopped: bool


def init_event_loop_scheduler():
    lock = Lock()
    delayed_task_lock = Lock()

    scheduler = EventLoopSchedulerImpl(
        immediate_tasks=deque(),
        delayed_tasks=[],
        lock=lock,
        delayed_task_lock=delayed_task_lock,
        condition=Condition(lock),
        _is_stopped=False,
    )

    Thread(target=scheduler.start_loop, daemon=True).start()

    return scheduler
    

@dataclassabc(frozen=False)
class MainSchedulerImpl(EventLoopSchedulerImpl, MainScheduler):
    _weight: int


def init_main_scheduler():
    lock = Lock()
    delayed_task_lock = Lock()

    return MainSchedulerImpl(
        immediate_tasks=deque(),
        delayed_tasks=[],
        lock=lock,
        delayed_task_lock=delayed_task_lock,
        condition=Condition(lock),
        _is_stopped=False,
        _weight=1,
    )


@dataclassabc(frozen=False)
class TrampolineImpl(Trampoline):
    queue: Deque[ScheduledTask]
    is_running: bool


def init_trampoline():
    return TrampolineImpl(
        queue=deque(),
        is_running=False,
    )


@dataclassabc(frozen=True)
class MainTrampolineImpl(MainTrampoline):
    queue: Deque[ScheduledTask]
    is_running: bool


def init_main_trampoline():
    return MainTrampolineImpl(
        queue=deque(),
        is_running=False,
    )


@dataclassabc(frozen=False)
class VirtualTimeSchedulerImpl(VirtualTimeScheduler):
    immediate_tasks: Deque[ScheduledTask]
    delayed_tasks: list[VirtualScheduledTask]
    lock: Lock
    delayed_task_lock: Lock
    _time: float
    _idle: bool
    start_datetime: datetime.datetime


def init_virtual_time_scheduler():
    return VirtualTimeSchedulerImpl(
        immediate_tasks=deque(),
        delayed_tasks=[],
        lock=Lock(),
        delayed_task_lock= Lock(),
        _idle=True,
        _time=0,
        start_datetime=datetime.datetime.now(),
    )


@dataclassabc(frozen=False)
class MainVirtualTimeSchedulerImpl(VirtualTimeSchedulerImpl, MainVirtualTimeScheduler):
    # is_stopped: bool
    _weight: int
    

def init_main_virtual_time_scheduler(
        # weight: int | None = None,
):
    # if weight is None:
    #     weight = 1

    return MainVirtualTimeSchedulerImpl(
        immediate_tasks=deque(),
        delayed_tasks=[],
        lock=Lock(),
        delayed_task_lock= Lock(),
        _idle=True,
        _time=0,
        _weight=0,
        start_datetime=datetime.datetime.now(),
    )


@dataclassabc(frozen=True)
class AsyncIOSchedulerImpl(AsyncIOScheduler):
    loop: asyncio.AbstractEventLoop
    

def init_asyncio_scheduler(
    loop: asyncio.AbstractEventLoop | None = None,
):
    if loop is None:
        loop = asyncio.new_event_loop()
        
    scheduler = AsyncIOSchedulerImpl(
        loop=loop,
    )

    Thread(target=scheduler.start_loop, daemon=True).start()

    return scheduler


@dataclassabc(frozen=True)
class MainAsyncIOSchedulerImpl(MainAsyncIOScheduler):
    loop: asyncio.AbstractEventLoop
    

def init_main_asyncio_scheduler(
    loop: asyncio.AbstractEventLoop | None = None,
):
    if loop is None:
        loop = asyncio.new_event_loop()

    return MainAsyncIOSchedulerImpl(
        loop=loop,
    )
