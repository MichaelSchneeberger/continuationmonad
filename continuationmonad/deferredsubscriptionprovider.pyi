from typing import Callable, Generator

from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.continuationmonadtree.deferredsubscription import DeferredSubscription
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate


class init_deferred_subscription_provider[U]:
    def __iter__(self) -> Generator[None, None, DeferredSubscription[U]]: ...
    def flat_map(
            self, func: Callable[[DeferredSubscription[U]], ContinuationMonad[ContinuationCertificate]],
    ) -> ContinuationMonad[U]: ...
