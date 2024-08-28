from typing import Callable, override, Generator

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline

class ContinuationMonad[U](ContinuationMonadNode[U]):
    # used for the donotation.do notation
    def __iter__(self) -> Generator[None, None, U]: ...
    @override
    def subscribe(self, trampoline: Trampoline, on_next: Callable[[Trampoline, U], Continuation]) -> Continuation: ...
    def copy(self, /, **changes) -> ContinuationMonad: ...

    # operations
    ############

    def flat_map[V](
        self, func: Callable[[U], ContinuationMonad[V]]
    ) -> ContinuationMonad[V]: ...
    def map[V](self, func: Callable[[U], V]) -> ContinuationMonad[V]: ...
