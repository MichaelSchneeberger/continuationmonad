from typing import Callable
from continuationmonad.continuationmonadtree.operations.join import Join
from dataclassabc import dataclassabc

from continuationmonad.utils.getstacklines import FrameSummary
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.continuationmonadtree.data.deferredsubscription import (
    DeferredSubscription,
)
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.continuationmonadtree.operations.scheduleon import ScheduleOn
from continuationmonad.continuationmonadtree.operations.connectsubscriptions import ConnectSubscriptions
from continuationmonad.continuationmonadtree.operations.defersubscription import DeferSubscription
from continuationmonad.continuationmonadtree.operations.flatmap import FlatMap
from continuationmonad.continuationmonadtree.operations.gettrampoline import (
    GetTrampoline,
)
from continuationmonad.continuationmonadtree.operations.map import Map
from continuationmonad.continuationmonadtree.operations.return_ import Return
from continuationmonad.continuationmonadtree.operations.trampolineon import (
    ScheduleTrampoline,
)


@dataclassabc(frozen=True)
class DeferSubscriptionImpl[U](DeferSubscription[U]):
    func: Callable[
        [DeferredSubscription[U]], ContinuationMonadNode[ContinuationCertificate]
    ]


def init_defer_subscription[U](
    func: Callable[
        [DeferredSubscription[U]], ContinuationMonadNode[ContinuationCertificate]
    ],
):
    return DeferSubscriptionImpl(
        func=func,
    )


@dataclassabc(frozen=True)
class FlatMapImpl[U, ChildU](FlatMap):
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
class GetTrampolineImpl(GetTrampoline):
    pass


def init_get_trampoline():
    return GetTrampolineImpl()


@dataclassabc(frozen=True)
class JoinImpl(Join):
    children: tuple[ContinuationMonadNode, ...]


def init_join(children: tuple[ContinuationMonadNode, ...]):
    return JoinImpl(children=children)


@dataclassabc(frozen=True)
class MapImpl[U, ChildU](Map):
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
class ReturnImpl[U](Return[U]):
    value: U


def init_return[U](value: U):
    return ReturnImpl(value=value)


@dataclassabc(frozen=True)
class ConnectSubscriptionsImpl(ConnectSubscriptions):
    child: ContinuationMonadNode
    subscriptions: tuple[DeferredSubscription, ...]


def init_connect_subscriptions(
    child: ContinuationMonadNode,
    subscriptions: tuple[DeferredSubscription, ...],
):
    return ConnectSubscriptionsImpl(
        child=child,
        subscriptions=subscriptions,
    )


@dataclassabc(frozen=True)
class ScheduleTrampolineImpl(ScheduleTrampoline):
    pass


def init_schedule_trampoline():
    return ScheduleTrampolineImpl()


@dataclassabc(frozen=True)
class ScheduleOnImpl(ScheduleOn):
    scheduler: Scheduler


def init_schedule_on(scheduler: Scheduler):
    return ScheduleOnImpl(scheduler=scheduler)
