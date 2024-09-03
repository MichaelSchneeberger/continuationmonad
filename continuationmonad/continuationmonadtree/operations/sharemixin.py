from abc import abstractmethod
from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.deferredsubscription import DeferredSubscription
from continuationmonad.continuationmonadtree.nodes import SingleChildContinuationMonadNode
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class SharedMixin[U](SingleChildContinuationMonadNode[tuple[ContinuationCertificate, ...], U]):
    def __str__(self) -> str:
        return f'shared({self.subscriptions})'

    @property
    @abstractmethod
    def subscriptions(self) -> tuple[DeferredSubscription[U], ...]: ...

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, tuple[ContinuationCertificate, ...]], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate:
        def n_on_next(n_trampoline: Trampoline, value: U):
            def gen_certificates():
                for connectable in self.subscriptions:
                    yield connectable.on_next(trampoline, value)

            certificates = tuple(gen_certificates())
            # continuation = ContinuationCertificate.merge_continuations(
            #     gen_continuations(),
            # )

            return on_next(n_trampoline, certificates)
        
        return self.child.subscribe(trampoline, n_on_next, cancellable)
