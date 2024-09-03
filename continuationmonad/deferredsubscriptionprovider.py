from typing import Callable

from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.continuationmonad.init import init_continuation_monad
from continuationmonad.continuationmonadtree.deferredsubscription import DeferredSubscription
from continuationmonad.continuationmonadtree.init import init_deferred
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate


class init_deferred_subscription_provider[U]:
    # def __iter__(self) -> Generator[None, None, DeferredSubscription[U]]: ...

    def flat_map(
            self, func: Callable[[DeferredSubscription[U]], ContinuationMonad[ContinuationCertificate]],
    ) -> ContinuationMonad[U]:
        return init_continuation_monad(init_deferred(func))

