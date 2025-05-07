from dataclasses import dataclass
from typing import Callable


from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.instantscheduler import InstantScheduler
from continuationmonad.scheduler.mainschedulermixin import MainScheduler
from continuationmonad.continuationmonadtree.to import (
    run as _run,
    fork as _fork,
)
from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad


def fork(
    source: ContinuationMonad[ContinuationCertificate],
    on_error: Callable[[Exception], ContinuationMonad[ContinuationCertificate]],
    scheduler: InstantScheduler,
    weight: int,
    cancellation: Cancellation | None = None,
) -> ContinuationCertificate:
    return _fork(
        source=source.child,
        on_error=on_error,
        scheduler=scheduler,
        weight=weight,
        cancellation=cancellation,
    )


def run[V](
    source: ContinuationMonad[V],
    scheduler: MainScheduler | None = None,
) -> V:
    return _run(
        source=source.child,
        scheduler=scheduler,
    )
