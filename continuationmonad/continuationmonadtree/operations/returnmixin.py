from abc import abstractmethod
from typing import Callable

from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline


class ReturnMixin[U](ContinuationMonadNode[U]):
    def __str__(self) -> str:
        return f'return({self.value})'
    
    @property
    @abstractmethod
    def value(self) -> U:
        ...

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, None], Continuation]
    ) -> Continuation:
        return on_next(trampoline, self.value)

