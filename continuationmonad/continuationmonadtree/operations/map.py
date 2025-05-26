from abc import abstractmethod
import traceback
from typing import Callable, override

from dataclassabc import dataclassabc

from continuationmonad.exceptions import ContinuationMonadOperatorException
from continuationmonad.utils.framesummary import (
    FrameSummary,
    FrameSummaryMixin,
)
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.observer import Observer
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import (
    SingleChildContinuationMonadNode,
)


@dataclassabc
class MapObserver[U, V](FrameSummaryMixin, Observer[U]):
    observer: Observer[V]
    func: Callable[[U], V]
    stack: tuple[FrameSummary, ...]
    raise_immediately: bool

    @override
    def on_success(self, trampoline: Trampoline, weight: int, item: U):
        try:
            mapped_item = self.func(item)

        except ContinuationMonadOperatorException as exception:
            if self.raise_immediately:
                raise

            exception = ContinuationMonadOperatorException(
                "\n".join(
                    (
                        exception.args[0],
                        self.to_execution_exception_message(traceback.format_exc()),
                    )
                )
            )
            return self.observer.on_error(trampoline, weight, exception)

        except Exception:
            if self.raise_immediately:
                raise ContinuationMonadOperatorException(
                    self.to_operator_exception_message(stack=self.stack)
                )
    
            exception = ContinuationMonadOperatorException(
                "\n".join(
                    (
                        self.to_execution_exception_message(traceback.format_exc()),
                        self.to_operator_exception_message(stack=self.stack),
                    )
                )
            )
            return self.observer.on_error(trampoline, weight, exception)

        return self.observer.on_success(trampoline, weight, mapped_item)

    @override
    def on_error(self, trampoline: Trampoline, weight: int, exception: Exception):
        return self.observer.on_error(trampoline, weight, exception)


class Map[U, V](FrameSummaryMixin, SingleChildContinuationMonadNode[U, V]):
    def __str__(self) -> str:
        return f"map({self.child}, {self.func})"

    @property
    @abstractmethod
    def func(self) -> Callable[[U], V]: ...

    @override
    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        return self.child.subscribe(
            args=args.copy(observer=MapObserver(
                observer=args.observer,
                func=self.func,
                stack=self.stack,
                raise_immediately=args.raise_immediately,
            ))
        )
