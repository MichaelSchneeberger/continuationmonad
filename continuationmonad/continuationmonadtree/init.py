from typing import Callable
from continuationmonad.continuationmonadtree.operations.scheduleonmixin import ScheduleOnMixin
from continuationmonad.continuationmonadtree.operations.sharemixin import SharedMixin
from continuationmonad.schedulers.scheduler import Scheduler
from dataclassabc import dataclassabc

from continuationmonad.continuationmonadtree.deferredsubscription import DeferredSubscription
from continuationmonad.continuationmonadtree.operations.deferredmixin import DeferredMixin
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.continuationmonadtree.operations.flatmapmixin import FlatMapMixin
from continuationmonad.continuationmonadtree.operations.gettrampolinemixin import GetTrampolineMixin
from continuationmonad.continuationmonadtree.operations.mapmixin import MapMixin
from continuationmonad.continuationmonadtree.operations.returnmixin import ReturnMixin
from continuationmonad.continuationmonadtree.operations.trampolineonmixin import ScheduleTrampolineMixin
from continuationmonad.utils.getstacklines import FrameSummary



@dataclassabc(frozen=True)
class DeferredImpl[U](DeferredMixin[U]):
    func: Callable[[DeferredSubscription[U]], ContinuationMonadNode[ContinuationCertificate]]


def init_deferred[U](
    func: Callable[[DeferredSubscription[U]], ContinuationMonadNode[ContinuationCertificate]],
):
    return DeferredImpl(
        func=func,
    )



@dataclassabc(frozen=True)
class FlatMapImpl[U, ChildU](FlatMapMixin):
    child: ContinuationMonadNode
    func: Callable[[ChildU], ContinuationMonadNode[U]]
    stack: tuple[FrameSummary, ...]


def init_flat_map[U, ChildU](
    child: ContinuationMonadNode,
    func: Callable[[ChildU], ContinuationMonadNode[U]],
    stack: tuple[FrameSummary, ...],
):
    return FlatMapImpl[U, ChildU](
        child=child,
        func=func,
        stack=stack,
    )


@dataclassabc(frozen=True)
class GetTrampolineImpl(GetTrampolineMixin):
    pass


def init_get_trampoline():
    return GetTrampolineImpl()


@dataclassabc(frozen=True)
class MapImpl[U, ChildU](MapMixin):
    child: ContinuationMonadNode
    func: Callable[[ChildU], U]
    stack: tuple[FrameSummary, ...]


def init_map[U, ChildU](
    child: ContinuationMonadNode,
    func: Callable[[ChildU], U],
    stack: tuple[FrameSummary, ...],
):
    return MapImpl[U, ChildU](
        child=child,
        func=func,
        stack=stack,
    )


@dataclassabc(frozen=True)
class ReturnImpl[U](ReturnMixin[U]):
    value: U


def init_return[U](value: U):
    return ReturnImpl(value=value)


@dataclassabc(frozen=True)
class SharedImpl(SharedMixin):
    child: ContinuationMonadNode
    subscriptions: tuple[DeferredSubscription, ...]


def init_shared(
        child: ContinuationMonadNode,
        subscriptions: tuple[DeferredSubscription, ...],
):
    return SharedImpl(
        child=child,
        subscriptions=subscriptions,
    )


@dataclassabc(frozen=True)
class ScheduleTrampolineImpl(ScheduleTrampolineMixin):
    pass


def init_schedule_trampoline():
    return ScheduleTrampolineImpl()


@dataclassabc(frozen=True)
class ScheduleOnImpl(ScheduleOnMixin):
    scheduler: Scheduler


def init_schedule_on(scheduler: Scheduler):
    return ScheduleOnImpl(scheduler=scheduler)
