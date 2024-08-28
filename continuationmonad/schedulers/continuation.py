from __future__ import annotations
from threading import RLock

from dataclassabc import dataclassabc

from continuationmonad.lockmixin import LockMixin


class ContinuationAtom(LockMixin):
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


@dataclassabc
class Continuation(LockMixin):
    atoms: list[ContinuationAtom]
    lock: RLock

    def __add__(self, other: Continuation):
        with self.lock:
            # create a new list
            atoms = self.atoms + other.atoms

        return Continuation(
            atoms=atoms,
            lock=self.lock,
        )

    def verify(self):
        while True:
            try:
                # remove atom from list
                atom = self.atoms.pop()
            except IndexError:
                raise Exception("No continuation available.")

            if atom.verify():
                break
