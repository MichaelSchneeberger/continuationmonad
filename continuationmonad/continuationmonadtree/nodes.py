from abc import ABC, abstractmethod

from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.init import init_main_scheduler, init_trampoline
from continuationmonad.continuationmonadtree.subscribeargs import (
    SubscribeArgs,
    init_subscribe_args,
)


class ContinuationMonadNode[V](ABC):
    @abstractmethod
    def subscribe(
        self,
        args: SubscribeArgs[V],
    ) -> ContinuationCertificate: ...
    
    def run(self) -> V:
        main_scheduler = init_main_scheduler()
        trampoline = init_trampoline()

        result = []

        def on_next(_, value):
            result.append(value)
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


class SingleChildContinuationMonadNode[U, V](ContinuationMonadNode[V]):
    """
    Represents a continuation monad node with a single child.
    """

    @property
    @abstractmethod
    def child(self) -> ContinuationMonadNode[U]: ...


class TwoChildrenContinuationMonadNode[L, R, U](ContinuationMonadNode[U]):
    """
    Represents a continuation monad node with two children.
    """

    @property
    @abstractmethod
    def left(self) -> ContinuationMonadNode[L]: ...

    @property
    @abstractmethod
    def right(self) -> ContinuationMonadNode[R]: ...


class MultiChildrenContinuationMonadNode[U, V](ContinuationMonadNode[V]):
    """
    Represents a continuation monad node with many children.
    """

    @property
    @abstractmethod
    def children(self) -> tuple[ContinuationMonadNode[U], ...]: ...
