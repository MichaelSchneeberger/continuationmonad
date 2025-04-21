from typing import Callable, Iterable

from continuationmonad.utils.framesummary import FrameSummary
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.schedulers.trampoline import Trampoline
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

def init_connect[U](
    child: ContinuationMonadNode[U],
    observers: Iterable[DeferredObserver[U]],
) -> Connect[U]: ...
def init_defer[U](
    func: Callable[[Trampoline, DeferredObserver[U]], ContinuationCertificate],
    stack: tuple[FrameSummary, ...],
) -> Defer[U]: ...
def init_flat_map[U, ChildU](
    child: ContinuationMonadNode[ChildU],
    func: Callable[[ChildU], ContinuationMonadNode[U]],
    stack: tuple[FrameSummary, ...],
) -> FlatMap[U, ChildU]: ...
def init_from_value[U](value: U) -> FromValue[U]: ...
def init_get_trampoline() -> GetTrampoline: ...
def init_map[U, ChildU](
    child: ContinuationMonadNode[ChildU],
    func: Callable[[ChildU], U],
    stack: tuple[FrameSummary, ...],
) -> Map[U, ChildU]: ...
def init_schedule_on(
    scheduler: Scheduler,
) -> ScheduleOn: ...

class init_zip[U]:
    def __new__(
        _,
        children: tuple[ContinuationMonadNode[U], ...],
    ) -> Zip[tuple[U, ...]]: ...

