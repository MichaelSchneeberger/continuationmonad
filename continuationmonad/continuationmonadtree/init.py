from typing import Callable
from dataclassabc import dataclassabc

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.continuationmonadtree.operations.flatmapmixin import FlatMapMixin
from continuationmonad.continuationmonadtree.operations.gettrampolinemixin import GetTrampolineMixin
from continuationmonad.continuationmonadtree.operations.mapmixin import MapMixin
from continuationmonad.continuationmonadtree.operations.returnmixin import ReturnMixin
from continuationmonad.continuationmonadtree.operations.trampolinemixin import TrampolineMixin
from continuationmonad.utils.getstacklines import FrameSummary



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
class TrampolineImpl(TrampolineMixin):
    pass


def init_trampoline():
    return TrampolineImpl()
