from abc import abstractmethod
from typing import Callable

from continuationmonad.lockmixin import LockMixin
from continuationmonad.schedulers.continuation import Continuation


class Scheduler(LockMixin):
    @abstractmethod
    def schedule(
        self,
        fn: Callable[[], Continuation],
    ) -> Continuation: ...

    def _create_continuation(self):
        ContinuationWithPermission = type(
            Continuation.__name__,
            Continuation.__mro__,
            Continuation.__dict__ | {"__permission__": True},
        )
        return ContinuationWithPermission(lock=self.lock)
