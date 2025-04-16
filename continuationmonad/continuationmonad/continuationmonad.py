from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generator, override

from continuationmonad.cancellation import Cancellation
from continuationmonad.continuationcertificate import ContinuationCertificate
from continuationmonad.continuationmonadtree.deferredobserver import DeferredObserver
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs, init_subscribe_args
from continuationmonad.continuationmonadtree.nodes import (
    ContinuationMonadNode,
    SingleChildContinuationMonadNode,
)
from continuationmonad.continuationmonadtree.init import (
    init_flat_map,
    init_map,
    init_connect,
)
from continuationmonad.schedulers.init import init_main_trampoline, init_trampoline
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.utils.framesummary import get_frame_summary


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
        )

        def trampoline_task():
            return self.subscribe(args=args)

        trampoline.run(trampoline_task)

        return result[0]

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
