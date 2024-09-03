from abc import abstractmethod
from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from dataclassabc import dataclassabc

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class DeferredSubscription[U]:
    @property
    @abstractmethod
    def on_next(self) -> Callable[[Trampoline, U], ContinuationCertificate]: ...

    @property
    @abstractmethod
    def cancellable(self) -> CancellableLeave | None: ...

    def connect(
        self, source: ContinuationMonadNode[U], trampoline: Trampoline
    ) -> ContinuationCertificate:
        return source.subscribe(trampoline, self.on_next, self.cancellable)


@dataclassabc(frozen=True)
class DeferredSubscriptionImpl[U](DeferredSubscription[U]):
    on_next: Callable[[Trampoline, U], ContinuationCertificate]
    cancellable: CancellableLeave | None


def init_deferred_subscription[U](
    on_next: Callable[[Trampoline, U], ContinuationCertificate],
    cancellable: CancellableLeave | None,
):
    return DeferredSubscriptionImpl(on_next=on_next, cancellable=cancellable)
