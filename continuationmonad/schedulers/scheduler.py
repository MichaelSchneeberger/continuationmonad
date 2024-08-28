from abc import abstractmethod
from typing import Callable

from continuationmonad.lockmixin import LockMixin
from continuationmonad.schedulers.continuation import Continuation, ContinuationAtom


class Scheduler(LockMixin):
    @abstractmethod
    def schedule(
        self,
        fn: Callable[[], Continuation],
    ) -> Continuation: ...

    def _create_continuation(self):
        ContinuationAtomWithPermission = type(
            ContinuationAtom.__name__,
            ContinuationAtom.__mro__,
            ContinuationAtom.__dict__ | {"__permission__": True},
        )
        atom = ContinuationAtomWithPermission(lock=self.lock)
        return Continuation(lock=self.lock, atoms=[atom])
