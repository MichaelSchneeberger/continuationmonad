from dataclasses import replace
from typing import override
from dataclassabc import dataclassabc

from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode


@dataclassabc(frozen=True)
class ContinuationMonadImpl[U](ContinuationMonad[U]):
    child: ContinuationMonadNode[U]

    def __str__(self) -> str:
        return f"ContinuationMonad({self.child})"

    @override
    def copy(self, /, **changes) -> ContinuationMonad[U]:
        return replace(self, **changes)


def init_continuation_monad[U](child: ContinuationMonadNode[U]):
    return ContinuationMonadImpl[U](child=child)
