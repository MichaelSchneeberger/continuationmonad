from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class GetTrampoline(ContinuationMonadNode[Trampoline]):
    def __str__(self) -> str:
        return 'get_trampoline()'

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, Trampoline], ContinuationCertificate],
        _: CancellableLeave | None = None,
    ) -> ContinuationCertificate:       
        return on_next(trampoline, trampoline)
