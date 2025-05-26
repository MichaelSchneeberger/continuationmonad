from abc import ABC, abstractmethod
from typing import override

from continuationmonad.scheduler.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.continuationmonadtree.subscribeargs import (
    SubscribeArgs,
)


class ContinuationMonadNode[V](ABC):
    @abstractmethod
    def subscribe(
        self,
        args: SubscribeArgs[V],
    ) -> ContinuationCertificate: ...


class ContinuationMonadLeave[U](ContinuationMonadNode[U]):
    @abstractmethod
    def _subscribe(
        self,
        args: SubscribeArgs[U],
    ) -> ContinuationCertificate: ...

    @override
    def subscribe(
        self,
        args: SubscribeArgs[U],
    ):
        def trampoline_task():
            certificate = self._subscribe(args=args)

            # if not isinstance(certificate, ContinuationCertificate):
            #     raise AssertionError(f'{self=}.subscribe returned {certificate}.')

            return certificate

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
