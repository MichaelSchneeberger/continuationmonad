from typing import Any, Callable, Iterable
from dataclassabc import dataclassabc

from continuationmonad.utils.framesummary import FrameSummary
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.instantscheduler import InstantScheduler
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.deferredobserver import DeferredObserver
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.continuationmonadtree.operations.zip import Zip
from continuationmonad.continuationmonadtree.sources.scheduleon import ScheduleOn
from continuationmonad.continuationmonadtree.operations.connect import (
    Connect,
)
from continuationmonad.continuationmonadtree.operations.defer import (
    Defer,
)
from continuationmonad.continuationmonadtree.operations.flatmap import FlatMap
from continuationmonad.continuationmonadtree.sources.gettrampoline import (
    GetTrampoline,
)
from continuationmonad.continuationmonadtree.operations.map import Map
from continuationmonad.continuationmonadtree.sources.fromvalue import FromValue


@dataclassabc(frozen=True)
class ConnectImpl(Connect):
    child: ContinuationMonadNode
    observers: Iterable[DeferredObserver]


def init_connect(child, observers):
    return ConnectImpl(
        child=child,
        observers=observers,
    )


@dataclassabc(frozen=True)
class DeferImpl[_](Defer):  # hide Impl classes in init.pyi for type hinting
    func: Callable[[Trampoline, DeferredObserver], ContinuationCertificate]
    stack: tuple[FrameSummary, ...]


def init_defer(
    func: Callable[[Trampoline, DeferredObserver], ContinuationCertificate],
    stack: tuple[FrameSummary, ...],
):
    return DeferImpl(
        func=func,
        stack=stack,
    )


@dataclassabc(frozen=True)
class FlatMapImpl[_, __](FlatMap):
    child: ContinuationMonadNode
    func: Callable[[Any], ContinuationMonadNode]
    stack: tuple[FrameSummary, ...]


def init_flat_map(
    child: ContinuationMonadNode,
    func: Callable[[Any], ContinuationMonadNode],
    stack: tuple[FrameSummary, ...],
):
    return FlatMapImpl(
        child=child,
        func=func,
        stack=stack,
    )


@dataclassabc(frozen=True)
class GetTrampolineImpl(GetTrampoline):
    pass


def init_get_trampoline():
    return GetTrampolineImpl()


@dataclassabc(frozen=True)
class ZipImpl[_](Zip):
    children: tuple[ContinuationMonadNode, ...]


def init_zip(children: Iterable[ContinuationMonadNode]):
    children = tuple(children)

    match len(children):
        case 0:
            raise AssertionError('No continuation monads provided. Cannot create a continuation monad.')
        
        case 1:
            return children
        
        case _:
            return ZipImpl(children=children)


@dataclassabc(frozen=True)
class MapImpl[_, __](Map):
    child: ContinuationMonadNode
    func: Callable
    stack: tuple[FrameSummary, ...]


def init_map(child, func, stack):
    return MapImpl(
        child=child,
        func=func,
        stack=stack,
    )


@dataclassabc(frozen=True)
class FromValueImpl[_](FromValue):
    value: Any


def init_from_value(value):
    return FromValueImpl(value)


@dataclassabc(frozen=True)
class ScheduleOnImpl(ScheduleOn):
    scheduler: InstantScheduler


def init_schedule_on(
    scheduler: InstantScheduler,
):
    return ScheduleOnImpl(
        scheduler=scheduler,
    )
