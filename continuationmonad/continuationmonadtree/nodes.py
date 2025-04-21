from abc import ABC, abstractmethod

from continuationmonad.cancellation import Cancellation
from continuationmonad.continuationmonadtree.subscribeargs import (
    SubscribeArgs,
    init_subscribe_args,
)
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.schedulers.init import init_main_trampoline
from continuationmonad.schedulers.trampoline import Trampoline


class ContinuationMonadNode[U](ABC):
    @abstractmethod
    def subscribe(
        self,
        args: SubscribeArgs,
    ) -> ContinuationCertificate: ...

    def run_on_trampoline(
        self,
        trampoline: Trampoline,
        weight: int,
        cancellation: Cancellation | None,
    ) -> ContinuationCertificate:
        args = init_subscribe_args(
            on_next=lambda _, c: c,
            trampoline=trampoline,
            cancellation=cancellation,
            weight=weight,
        )

        def trampoline_task():
            return self.subscribe(args=args)

        return trampoline.schedule(trampoline_task, weight=weight)
    
    def run(self):
        trampoline = init_main_trampoline()

        result = [None]

        def on_next(_, value):
            result[0] = value
            return trampoline.stop()

        args = init_subscribe_args(
            on_next=on_next,
            trampoline=trampoline,
            weight=1,
        )

        def trampoline_task():
            return self.subscribe(args=args)

        trampoline.run(trampoline_task)

        return result[0]


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
