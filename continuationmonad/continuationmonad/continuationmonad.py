from __future__ import annotations

from abc import abstractmethod
from typing import Callable, override

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.data.deferredsubscription import DeferredSubscription
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode, SingleChildContinuationMonadNode
from continuationmonad.continuationmonadtree.init import (
    # init_defer_continuation,
    init_connect_subscriptions,
    init_flat_map,
    init_map,
)
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
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
        on_next: Callable[[Trampoline, U], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate:
        return self.child.subscribe(trampoline=trampoline, on_next=on_next, cancellable=cancellable)

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

    def connect(self, subscriptions: tuple[DeferredSubscription, ...]):
        return self.copy(child=init_connect_subscriptions(child=self.child, subscriptions=subscriptions))
