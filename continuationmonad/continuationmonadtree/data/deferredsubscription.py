from typing import Callable, NamedTuple

from continuationmonad.cancellable import CancellableLeave

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class DeferredSubscription[U](NamedTuple):
    on_next: Callable[[Trampoline, U], ContinuationCertificate]
    cancellable: CancellableLeave | None

    def connect(
        self, source: ContinuationMonadNode[U], trampoline: Trampoline
    ) -> ContinuationCertificate:
        return source.subscribe(trampoline, self.on_next, self.cancellable)


def init_deferred_subscription[U](
    on_next: Callable[[Trampoline, U], ContinuationCertificate],
    cancellable: CancellableLeave | None,
):
    return DeferredSubscription(on_next=on_next, cancellable=cancellable)
