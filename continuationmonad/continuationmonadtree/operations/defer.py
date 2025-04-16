from abc import abstractmethod
from typing import Callable

from continuationmonad.continuationmonadtree.deferredobserver import DeferredObserver
from continuationmonad.exceptions import ContinuationMonadOperatorException
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.utils.framesummary import FrameSummaryMixin


class Defer[U](FrameSummaryMixin, ContinuationMonadNode[U]):
    def __str__(self) -> str:
        return "defer()"

    @property
    @abstractmethod
    def func(
        self,
    ) -> Callable[
        [Trampoline, DeferredObserver], ContinuationMonadNode[ContinuationCertificate]
    ]: ...

    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        deferred_observer = DeferredObserver(
            on_next=args.on_next,
            weight=args.weight,
            cancellation=args.cancellation,
        )

        try:
            continuation = self.func(args.trampoline, deferred_observer)
            
        except ContinuationMonadOperatorException:
            raise

        except Exception:
            raise ContinuationMonadOperatorException(
                self.to_operator_exception_message(stack=self.stack)
            )

        return continuation.subscribe(
            args=args.copy(
                on_next=lambda _, v: v,
            )
        )
