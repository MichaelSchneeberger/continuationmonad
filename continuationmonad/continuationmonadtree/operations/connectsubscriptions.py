from abc import abstractmethod
from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.data.deferredsubscription import DeferredSubscription
from continuationmonad.continuationmonadtree.nodes import SingleChildContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class ConnectSubscriptions[U](SingleChildContinuationMonadNode[tuple[ContinuationCertificate, ...], U]):
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
                for subscription in self.subscriptions:

                    def request_next_item(subscription=subscription):
                        return subscription.on_next(trampoline, value)
                    
                    yield trampoline.schedule(request_next_item)

            certificates = tuple(gen_certificates())

            return on_next(n_trampoline, certificates)
        
        return self.child.subscribe(trampoline, n_on_next, cancellable)
