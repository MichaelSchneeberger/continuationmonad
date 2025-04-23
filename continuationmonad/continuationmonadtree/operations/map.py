from abc import abstractmethod
from typing import Callable

from continuationmonad.exceptions import ContinuationMonadOperatorException
from continuationmonad.utils.framesummary import (
    FrameSummaryMixin,
)
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import (
    SingleChildContinuationMonadNode,
)


class Map[U, ChildU](FrameSummaryMixin, SingleChildContinuationMonadNode[U, ChildU]):
    def __str__(self) -> str:
        return f"map({self.child}, {self.func})"

    @property
    @abstractmethod
    def func(self) -> Callable[[ChildU], U]: ...

    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        def n_on_next(n_trampoline: Trampoline, value: ChildU):
            try:
                n_value = self.func(value)
                
            except ContinuationMonadOperatorException:
                raise

            except Exception:
                raise ContinuationMonadOperatorException(
                    self.to_operator_exception_message(stack=self.stack)
                )

            return args.on_next(n_trampoline, n_value)

        return self.child.subscribe(args=args.copy(on_next=n_on_next))
