from abc import abstractmethod
from typing import Iterable

from continuationmonad.continuationmonadtree.deferredobserver import DeferredObserver
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import SingleChildContinuationMonadNode
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


class Connect[U](SingleChildContinuationMonadNode[U, tuple[ContinuationCertificate, ...]]):
    def __str__(self) -> str:
        return f'connect({self.observers})'

    @property
    @abstractmethod
    def observers(self) -> Iterable[DeferredObserver]: ...

    def subscribe(
        self,
        args: SubscribeArgs[tuple[ContinuationCertificate, ...]],
    ) -> ContinuationCertificate:
        def on_next(n_trampoline: Trampoline, value: U):
            def gen_certificates():
                for observer in self.observers:

                    def request_next_item(observer=observer):
                        return observer.on_next(n_trampoline, value)
                    
                    yield n_trampoline.schedule(request_next_item, weight=observer.weight)

            certificates = tuple(gen_certificates())

            return args.on_next(n_trampoline, certificates)
        
        return self.child.subscribe(args=args.copy(on_next=on_next))
