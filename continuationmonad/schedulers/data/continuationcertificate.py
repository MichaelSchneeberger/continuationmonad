from __future__ import annotations
from threading import RLock


class ContinuationCertificate:
    __permission__ = False

    def __init__(self, lock: RLock):
        assert self.__permission__
        self.__verified__ = False

        self._lock = lock

    @property
    def lock(self) -> RLock:
        return self._lock

    def verify(self) -> bool:
        """
        A continuation can be verified exactly once.
        """

        with self._lock:
            # assert not self.__verified__, 'A continuation can only be verified once.'
            p_verified = self.__verified__
            self.__verified__ = True

        return not p_verified


def init_continuation_continuation(
    lock: RLock,
):
    return ContinuationCertificate(
        lock=lock,
    )
