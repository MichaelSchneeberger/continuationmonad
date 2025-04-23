from dataclasses import dataclass, replace
from typing import Any, Callable

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


@dataclass
class SubscribeArgs[U]:
    on_next: Callable[[Trampoline, U], ContinuationCertificate]

    # weight of the continuation certificate returned by the subscribe method
    weight: int

    # Allows to cancel the continuation. The cancellation is not executed immediately, 
    # but only when a new task associated with the continuation is scheduled.
    cancellation: Cancellation | None

    # ensure that no item is emitted before subscribe method returns
    trampoline: Trampoline

    def copy[V](
        self, /, 
        on_next: Callable[[Trampoline, V], ContinuationCertificate] | None = None, 
        cancellation: Cancellation | None = None,
        trampoline: Trampoline | None = None,
        weight: int | None = None,
        **others,
    ):
        def gen_args():
            if on_next is not None:
                yield 'on_next', on_next
            if cancellation is not None:
                yield 'cancellation', cancellation
            if trampoline is not None:
                yield 'trampoline', trampoline
            if weight is not None:
                yield 'weight', weight

        args = dict(gen_args()) | others
        return replace(self, **args)


def init_subscribe_args(
    on_next: Callable[[Trampoline, Any], ContinuationCertificate],
    trampoline: Trampoline,
    weight: int,
    cancellation: Cancellation | None = None,
):
    return SubscribeArgs(
        on_next=on_next,
        weight=weight,
        cancellation=cancellation,
        trampoline=trampoline,
    )
