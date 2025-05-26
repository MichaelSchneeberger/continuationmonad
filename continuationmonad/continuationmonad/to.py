from typing import Callable


from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.instantscheduler import InstantScheduler
from continuationmonad.scheduler.mainschedulermixin import MainSchedulerMixin
from continuationmonad.continuationmonadtree.to import (
    run as _run,
    fork as _fork,
    to_asyncio as _to_asyncio,
)
from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.scheduler.schedulers.asyncioscheduler import AsyncIOScheduler


def fork(
    source: ContinuationMonad[ContinuationCertificate],
    on_error: Callable[[Exception], ContinuationMonad[ContinuationCertificate]],
    scheduler: InstantScheduler,
    weight: int,
    cancellation: Cancellation | None = None,
):
    return _fork(
        source=source.child,
        on_error=on_error,
        scheduler=scheduler,
        weight=weight,
        cancellation=cancellation,
    )


def run[V](
    source: ContinuationMonad[V],
    scheduler: MainSchedulerMixin | None = None,
):
    return _run(
        source=source.child,
        scheduler=scheduler,
    )


def to_asyncio[U](
    source: ContinuationMonad[U],
    scheduler: AsyncIOScheduler,
):
    return _to_asyncio(
        source=source.child,
        scheduler=scheduler,
    )
