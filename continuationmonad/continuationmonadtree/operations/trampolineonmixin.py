from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class ScheduleTrampolineMixin(ContinuationMonadNode[Trampoline]):
    def __str__(self) -> str:
        return 'trampoline()'

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, Trampoline], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate:
        def trampoline_action():
            return on_next(trampoline, trampoline)
        return trampoline.schedule(trampoline_action, cancellable)
