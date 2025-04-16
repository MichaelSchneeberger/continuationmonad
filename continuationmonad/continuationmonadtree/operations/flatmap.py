from abc import abstractmethod
from typing import Callable

from continuationmonad.exceptions import ContinuationMonadOperatorException
from continuationmonad.utils.framesummary import (
    FrameSummaryMixin,
)
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import (
    ContinuationMonadNode,
    SingleChildContinuationMonadNode,
)


class FlatMap[U, ChildU](
    FrameSummaryMixin, SingleChildContinuationMonadNode[U, ChildU]
):
    def __str__(self) -> str:
        return f"flat_map({self.child}, {self.func})"

    @property
    @abstractmethod
    def func(self) -> Callable[[ChildU], ContinuationMonadNode[U]]: ...

    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        def n_on_next(n_trampoline: Trampoline, value: ChildU):

            try:
                continuation = self.func(value)
                
            except ContinuationMonadOperatorException:
                raise

            except Exception:
                raise ContinuationMonadOperatorException(
                    self.to_operator_exception_message(stack=self.stack)
                )
            
            try:
                certificate = continuation.subscribe(
                    args=args.copy(
                        on_next=args.on_next,
                        trampoline=n_trampoline,
                    )
                )

            except ContinuationMonadOperatorException:
                raise

            except Exception:
                raise ContinuationMonadOperatorException(
                    to_operator_exception_message(stack=self.stack)
                )

            return certificate

        return self.child.subscribe(args=args.copy(on_next=n_on_next))





# @dataclassabc
# class FlatMapObserver[ChildU, U](FrameSummaryMixin, Observer):
#     observer: Observer
#     func: Callable[[ChildU], ContinuationMonadNode[U]]
#     stack: tuple[FrameSummary, ...]
#     weight: int
#     cancellation: IsCancelled | None

#     def on_next(self, trampoline: Trampoline, value: ChildU):

#         try:
#             continuation = self.func(value)

#         except ContinuationMonadOperatorException:
#             raise

#         except Exception:
#             msg = to_operator_exception_message(stack=self.stack)
#             raise ContinuationMonadOperatorException(f'{msg}')
        
#         try:
#             certificate = continuation.subscribe(
#                 args=init_subscribe_args(
#                     observer=self.observer,
#                     trampoline=trampoline,
#                 )
#             )

#         except ContinuationMonadOperatorException:
#             raise

#         except Exception:
#             msg = to_operator_exception_message(stack=self.stack)
#             raise ContinuationMonadOperatorException(f'{msg}')

#         return certificate


# class FlatMap[U, ChildU](
#     FrameSummaryMixin, SingleChildContinuationMonadNode[U, ChildU]
# ):
#     def __str__(self) -> str:
#         return f"flat_map({self.child}, {self.func})"

#     @property
#     @abstractmethod
#     def func(self) -> Callable[[ChildU], ContinuationMonadNode[U]]: ...

#     def subscribe(
#         self,
#         args: SubscribeArgs,
#     ):

#         return self.child.subscribe(args=init_subscribe_args(
#             observer=FlatMapObserver(
#                 observer=args.observer,
#                 weight=args.weight,
#                 cancellation=args.cancellation,
#                 func=self.func,
#                 stack=self.stack,
#             ),
#             trampoline=args.trampoline,
#         ))
