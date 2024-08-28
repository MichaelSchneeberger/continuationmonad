from __future__ import annotations

from abc import abstractmethod
from typing import Callable, override

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode, SingleChildContinuationMonadNode
from continuationmonad.continuationmonadtree.init import (
    init_flat_map,
    init_map,
)
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.utils.getstacklines import get_frame_summary


class ContinuationMonad[U](
    SingleChildContinuationMonadNode[U, U]
):
    """
    The StateMonad class implements a dot notation syntax, providing convenient methods to define and 
    chain monadic operations.
    """

    @override
    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, U], Continuation]
    ) -> Continuation:
        return self.child.subscribe(trampoline=trampoline, on_next=on_next)

    @abstractmethod
    def copy(self, /, **changes) -> ContinuationMonad: ...

    # operations
    ############

    def flat_map[V](
        self, func: Callable[[V], ContinuationMonadNode[U]]
    ):
        return self.copy(child=init_flat_map(child=self.child, func=func, stack=get_frame_summary()))

    def map[V](self, func: Callable[[U], V]):
        return self.copy(child=init_map(child=self.child, func=func, stack=get_frame_summary()))
