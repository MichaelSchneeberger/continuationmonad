from abc import ABC, abstractmethod

from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.init import init_main_scheduler, init_trampoline
from continuationmonad.continuationmonadtree.subscribeargs import (
    SubscribeArgs,
    init_subscribe_args,
)


class ContinuationMonadNode[U](ABC):
    @abstractmethod
    def subscribe(
        self,
        args: SubscribeArgs,
    ) -> ContinuationCertificate: ...
    
    def run(self):
        main_scheduler = init_main_scheduler()
        trampoline = init_trampoline()

        result = [None]

        def on_next(_, value):
            result[0] = value
            return main_scheduler.stop()

        args = init_subscribe_args(
            on_next=on_next,
            trampoline=trampoline,
            weight=1,
        )

        def schedule_task():
            def trampoline_task():
                return self.subscribe(args=args)

            return trampoline.run(trampoline_task, weight=1)
        main_scheduler.run(schedule_task)

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
