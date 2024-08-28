from abc import abstractmethod
from threading import RLock

from continuationmonad.lockmixin import LockMixin


class Continuation(LockMixin):
    __permission__ = False
    
    def __init__(self, lock: RLock):
        assert self.__permission__
        self.__verified__ = False

        self._lock= lock

    @property
    def lock(self) -> RLock:
        return self._lock

    def verify(self):
        """
        A continuation can be verified exactly once.
        """

        assert not self.__verified__, 'A continuation can only be verified once.'
        self.__verified__ = True


class ContinuationCollection(LockMixin):
    continuations: list[Continuation]



type MaybeContinuation = Continuation | None

def sort_continuations(left: MaybeContinuation, right: MaybeContinuation):
    match (left, right):
        case (Continuation(), _):
            return left, right
        case _:
            return right, left
