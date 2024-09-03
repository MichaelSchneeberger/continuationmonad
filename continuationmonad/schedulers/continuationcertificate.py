from __future__ import annotations
from threading import RLock
from typing import Iterable

from dataclassabc import dataclassabc

from continuationmonad.lockmixin import LockMixin


class ContinuationCertificate(LockMixin):
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

# @dataclassabc
# class ContinuationCertificate:
#     atoms: list[ContinuationCertificateAtom]
#     lock: RLock

#     def __add__(self, other: ContinuationCertificate):
#         return self.merge_continuations(
#             continuations=(self, other),
#         )
    
#     # def append(self, other: Continuation):
#     #     self.atoms.extend(other.atoms)
#     #     return self

#     def verify(self):
#         while True:
#             try:
#                 # remove atom from list
#                 atom = self.atoms.pop()
#             except IndexError:
#                 raise Exception("No continuation available.")

#             if atom.verify():
#                 break

#     @staticmethod
#     def merge_continuations(continuations: Iterable[ContinuationCertificate]):
#         continuation_tuple = tuple(continuations)

#         def gen_atoms():
#             for continuation in continuation_tuple:
#                 with continuation.lock:
#                     n_atoms = list(continuation.atoms)  # copy atoms
                
#                 yield from n_atoms
        
#         return init_continuation(
#             atoms=list(gen_atoms()),
#             lock=continuation_tuple[0].lock,
#         )



# def init_continuation(
#     atoms: list[ContinuationCertificateAtom],
#     lock: RLock,
# ):
#     return ContinuationCertificate(
#         atoms=atoms,
#         lock=lock,
#     )
