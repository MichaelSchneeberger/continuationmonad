from abc import ABC, abstractmethod

from continuationmonad.continuationmonadtree.subscribeargs import (
    SubscribeArgs,
)
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)


class ContinuationMonadNode[U](ABC):
    @abstractmethod
    def subscribe(
        self,
        args: SubscribeArgs,
    ) -> ContinuationCertificate: ...


class SingleChildContinuationMonadNode[U, ChildU](ContinuationMonadNode[U]):
    """
    Represents a continuation monad node with a single child.
    """

    @property
    @abstractmethod
    def child(self) -> ContinuationMonadNode[ChildU]: ...


class TwoChildrenContinuationMonadNode[U, L, R](ContinuationMonadNode[U]):
    """
    Represents a continuation monad node with two children.
    """

    @property
    @abstractmethod
    def left(self) -> ContinuationMonadNode[L]: ...

    @property
    @abstractmethod
    def right(self) -> ContinuationMonadNode[R]: ...


class MultiChildrenContinuationMonadNode[U, UChild](ContinuationMonadNode[U]):
    """
    Represents a continuation monad node with many children.
    """

    @property
    @abstractmethod
    def children(self) -> tuple[ContinuationMonadNode[UChild], ...]: ...
