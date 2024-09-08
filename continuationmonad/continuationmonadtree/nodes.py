from abc import ABC, abstractmethod
from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class ContinuationMonadNode[U](ABC):
    @abstractmethod
    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, U], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate: ...


class SingleChildContinuationMonadNode[U, ChildU](ContinuationMonadNode[U]):
    """
    Represents a state monad node with a single child.
    """

    @property
    @abstractmethod
    def child(self) -> ContinuationMonadNode[ChildU]: ...


class TwoChildrenContinuationMonadNode[U, L, R](ContinuationMonadNode[U]):
    """
    Represents a state monad node with two children.
    """

    @property
    @abstractmethod
    def left(self) -> ContinuationMonadNode[L]: ...

    @property
    @abstractmethod
    def right(self) -> ContinuationMonadNode[R]: ...


class MultiChildrenContinuationMonadNode[U, UChild](ContinuationMonadNode[U]):
    """
    Represents a state monad node with two children.
    """

    @property
    @abstractmethod
    def children(self) -> tuple[ContinuationMonadNode[UChild], ...]: ...
