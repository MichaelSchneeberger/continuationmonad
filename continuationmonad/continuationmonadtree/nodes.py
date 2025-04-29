from abc import ABC, abstractmethod

from continuationmonad.continuationmonadtree.observer import Observer
from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.scheduler.init import init_main_scheduler, init_trampoline
from continuationmonad.continuationmonadtree.subscribeargs import (
    SubscribeArgs,
    init_subscribe_args,
)
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


class ContinuationMonadNode[V](ABC):
    @abstractmethod
    def subscribe(
        self,
        args: SubscribeArgs[V],
    ) -> ContinuationCertificate: ...
    
    def run(self) -> V:
        main_scheduler = init_main_scheduler()
        trampoline = init_trampoline()

        received_exception = []
        received_item = []

        class MainObserver(Observer):
            def on_success(self, _, item: V) -> ContinuationCertificate:
                received_item.append(item)
                return main_scheduler.stop()

            def on_error(self, _, exception: Exception) -> ContinuationCertificate:
                received_exception.append(exception)
                return main_scheduler.stop()

        args = init_subscribe_args(
            observer=MainObserver(),
            trampoline=trampoline,
            weight=1,
        )

        def schedule_task():
            def trampoline_task():
                return self.subscribe(args=args)

            return trampoline.run(trampoline_task, weight=1)
        main_scheduler.run(schedule_task)

        if received_exception:
            raise received_exception[0]

        return received_item[0]


class ContinuationMonadLeave[U](ContinuationMonadNode[U]):
    @abstractmethod
    def _subscribe(
        self,
        args: SubscribeArgs[U],
    ) -> ContinuationCertificate: ...

    def subscribe(
        self,
        args: SubscribeArgs[U],
    ) -> ContinuationCertificate:
        def trampoline_task():
            return self._subscribe(args=args)

        return args.trampoline.schedule(
            task=trampoline_task,
            weight=args.weight,
            cancellation=args.cancellation,
        )


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
