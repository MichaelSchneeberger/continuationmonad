from typing import Callable

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline


class GetTrampolineMixin(ContinuationMonadNode[Trampoline]):
    def __str__(self) -> str:
        return 'get_trampoline()'

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, Trampoline], Continuation]
    ) -> Continuation:       
        return on_next(trampoline, trampoline)
