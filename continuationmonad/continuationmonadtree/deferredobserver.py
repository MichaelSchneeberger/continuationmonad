from dataclasses import dataclass
from typing import Callable

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


@dataclass
class DeferredObserver[U]:
    on_next: Callable[[Trampoline, U], ContinuationCertificate]
    weight: int
    cancellation: Cancellation | None
