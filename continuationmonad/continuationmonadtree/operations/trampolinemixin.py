from typing import Callable

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline


class TrampolineMixin(ContinuationMonadNode[None]):
    def __str__(self) -> str:
        return 'trampoline()'

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, None], Continuation]
    ) -> Continuation:       
        def trampoline_action():
            return on_next(trampoline, None)
        return trampoline.schedule(trampoline_action)
