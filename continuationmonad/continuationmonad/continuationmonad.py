from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generator, override

from continuationmonad.utils.framesummary import get_frame_summary
from continuationmonad.cancellation import Cancellation
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.continuationcertificate import ContinuationCertificate
from continuationmonad.continuationmonadtree.nodes import (
    ContinuationMonadNode,
    SingleChildContinuationMonadNode,
)
from continuationmonad.continuationmonadtree.deferredobserver import DeferredObserver
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.init import (
    init_flat_map,
    init_map,
    init_connect,
)


class ContinuationMonad[U](SingleChildContinuationMonadNode[U, U]):
    """
    The StateMonad class implements a dot notation syntax, providing convenient methods to define and
    chain monadic operations.
    """

    # used for the donotation.do notation
    def __iter__(self) -> Generator[None, None, U]: ...

    @override
    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        return self.child.subscribe(args=args)

    def run_on_trampoline(
        self,
        trampoline: Trampoline,
        weight: int,
        cancellation: Cancellation | None,
    ) -> ContinuationCertificate:
        return self.child.run_on_trampoline(
            trampoline=trampoline,
            weight=weight,
            cancellation=cancellation,
        )

    def run(self):
        return self.child.run()

    @abstractmethod
    def copy[V](self, child: ContinuationMonadNode[V]) -> ContinuationMonad[V]: ...

    # operations
    ############

    def connect(self, observers: tuple[DeferredObserver, ...]):
        return self.copy(
            child=init_connect(child=self.child, observers=observers)
        )

    def flat_map[V](self, func: Callable[[U], ContinuationMonadNode[V]]):
        return self.copy(
            child=init_flat_map(child=self.child, func=func, stack=get_frame_summary())
        )

    def map[V](self, func: Callable[[U], V]):
        return self.copy(
            child=init_map(child=self.child, func=func, stack=get_frame_summary())
        )
