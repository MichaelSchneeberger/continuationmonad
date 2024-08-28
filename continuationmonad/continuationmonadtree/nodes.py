from abc import ABC, abstractmethod
from typing import Callable
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline


class ContinuationMonadNode[U](ABC):
    @abstractmethod
    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, U], Continuation]
    ) -> Continuation: ...


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
