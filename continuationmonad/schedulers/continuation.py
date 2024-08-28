from __future__ import annotations
from threading import RLock
from typing import Iterable

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
        return self.merge_continuations(
            continuations=(self, other),
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

    @staticmethod
    def merge_continuations(continuations: Iterable[Continuation], lock: RLock):
        def gen_atoms():
            for continuation in continuations:
                with continuation.lock:
                    n_atoms = list(continuation.atoms)  # copy atoms
                
                yield from n_atoms
        
        return Continuation(
            atoms=list(gen_atoms()),
            lock=lock
        )



def init_continuation(
    atoms: list[ContinuationAtom],
    lock: RLock,
):
    return Continuation(
        atoms=atoms,
        lock=lock,
    )
