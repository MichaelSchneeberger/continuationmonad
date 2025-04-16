from dataclasses import dataclass
from typing import Callable

from continuationmonad.cancellation import Cancellation
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.schedulers.trampoline import Trampoline


@dataclass
class DeferredObserver[U]:
    on_next: Callable[[Trampoline, U], ContinuationCertificate]
    weight: int
    cancellation: Cancellation | None
