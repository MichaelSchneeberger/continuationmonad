from abc import abstractmethod
import traceback
from typing import Callable

from dataclassabc import dataclassabc

from continuationmonad.exceptions import ContinuationMonadOperatorException
from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.utils.framesummary import (
    FrameSummary,
    FrameSummaryMixin,
)
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import (
    SubscribeArgs,
    init_subscribe_args,
)
from continuationmonad.continuationmonadtree.nodes import (
    ContinuationMonadNode,
    SingleChildContinuationMonadNode,
)
from continuationmonad.continuationmonadtree.observer import Observer


@dataclassabc
class FlatMapObserver[U, V](FrameSummaryMixin, Observer[U]):
    observer: Observer[V]
    func: Callable[[U], ContinuationMonadNode[V]]
    stack: tuple[FrameSummary, ...]
    weight: int
    cancellation: Cancellation | None

    def on_success(self, trampoline: Trampoline, item: U):
        try:
            continuation = self.func(item)

        except ContinuationMonadOperatorException as exception:
            exception = ContinuationMonadOperatorException(
                "\n".join(
                    (
                        exception.args[0],
                        self.to_execution_exception_message(traceback.format_exc()),
                    )
                )
            )
            return self.observer.on_error(exception)

        except Exception:
            exception = ContinuationMonadOperatorException(
                "\n".join(
                    (
                        self.to_execution_exception_message(traceback.format_exc()),
                        self.to_operator_exception_message(stack=self.stack),
                    )
                )
            )
            return self.observer.on_error(exception)

        try:
            certificate = continuation.subscribe(
                args=init_subscribe_args(
                    observer=self.observer,
                    trampoline=trampoline,
                    weight=self.weight,
                    cancellation=self.cancellation,
                )
            )

        except ContinuationMonadOperatorException as exception:
            exception = ContinuationMonadOperatorException(
                "\n".join(
                    (
                        exception.args[0],
                        self.to_execution_exception_message(traceback.format_exc()),
                    )
                )
            )
            return self.observer.on_error(exception)

        except Exception:
            exception = ContinuationMonadOperatorException(
                "\n".join(
                    (
                        self.to_execution_exception_message(traceback.format_exc()),
                        self.to_operator_exception_message(stack=self.stack),
                    )
                )
            )
            return self.observer.on_error(exception)

        return certificate

    def on_error(self, exception: Exception):
        return self.observer.on_error(exception)


class FlatMap[U, V](FrameSummaryMixin, SingleChildContinuationMonadNode[U, V]):
    def __str__(self) -> str:
        return f"flat_map({self.child}, {self.func})"

    @property
    @abstractmethod
    def func(self) -> Callable[[U], ContinuationMonadNode[V]]: ...

    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        return self.child.subscribe(
            args=args.copy(
                observer=FlatMapObserver(
                    observer=args.observer,
                    func=self.func,
                    stack=self.stack,
                    weight=args.weight,
                    cancellation=args.cancellation,
                )
            )
        )
