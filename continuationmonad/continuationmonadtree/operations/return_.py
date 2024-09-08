from abc import abstractmethod
from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class Return[U](ContinuationMonadNode[U]):
    def __str__(self) -> str:
        return f'return({self.value})'
    
    @property
    @abstractmethod
    def value(self) -> U:
        ...

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, U], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate:
        return on_next(trampoline, self.value)
