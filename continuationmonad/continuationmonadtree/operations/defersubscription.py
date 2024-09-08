from abc import abstractmethod
from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.data.deferredsubscription import DeferredSubscription, init_deferred_subscription
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class DeferSubscription[U](ContinuationMonadNode[U]):
    def __str__(self) -> str:
        return 'deferred()'

    @property
    @abstractmethod
    def func(self) -> Callable[[DeferredSubscription[U]], ContinuationMonadNode[ContinuationCertificate]]: ...

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, U], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate:
        subscription = init_deferred_subscription(
            on_next=on_next,
            cancellable=cancellable,
        )
        continuation = self.func(subscription)
        return continuation.subscribe(trampoline=trampoline, on_next=lambda _, v: v)
