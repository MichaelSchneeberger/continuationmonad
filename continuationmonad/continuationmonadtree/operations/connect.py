from abc import abstractmethod

from continuationmonad.continuationmonadtree.deferredobserver import DeferredObserver
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import SingleChildContinuationMonadNode
from continuationmonad.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class Connect[U](SingleChildContinuationMonadNode[tuple[ContinuationCertificate, ...], U]):
    def __str__(self) -> str:
        return f'connect({self.observers})'

    @property
    @abstractmethod
    def observers(self) -> tuple[DeferredObserver, ...]: ...

    def subscribe(
        self,
        args: SubscribeArgs,
    ) -> ContinuationCertificate:
        def n_on_next(n_trampoline: Trampoline, value: U):
            def gen_certificates():
                for observer in self.observers:

                    def request_next_item(observer=observer):
                        return observer.on_next(n_trampoline, value)
                    
                    yield n_trampoline.schedule(request_next_item, weight=observer.weight)

            certificates = tuple(gen_certificates())

            return args.on_next(n_trampoline, certificates)
        
        return self.child.subscribe(args=args.copy(
            on_next=n_on_next,
        ))
