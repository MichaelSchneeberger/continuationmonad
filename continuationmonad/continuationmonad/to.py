from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.schedulers.trampoline import Trampoline


def fork(
        continuation: Callable[[], ContinuationMonad[ContinuationCertificate]],
        scheduler: Scheduler,
        cancellable: CancellableLeave | None = None,
):
    def scheduled_item():
        def on_next(_, value: ContinuationCertificate):
            return value

        def trampoline_action():
            return continuation().subscribe(
                on_next=on_next,
                trampoline=trampoline,
                cancellable=cancellable
            )
        
        if isinstance(scheduler, Trampoline):
            trampoline = scheduler
            return trampoline_action()
        
        else:
            trampoline = Trampoline()
            return trampoline.schedule(trampoline_action)

    return scheduler.schedule(scheduled_item)
