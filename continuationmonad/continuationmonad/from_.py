from typing import Callable, Iterable

from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.continuationmonad.init import init_continuation_monad

from continuationmonad.continuationmonadtree.deferredobserver import DeferredObserver
from continuationmonad.continuationmonadtree.init import (
    init_zip,
    init_from_value,
    init_get_trampoline,
    init_defer,
    init_schedule_on,
)
from continuationmonad.continuationcertificate import (
    ContinuationCertificate,
)
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.utils.framesummary import get_frame_summary


# def accumulate[S, T](
#     func: Callable[[T, S], ContinuationMonad[T]],
#     iterable: Iterable[S],
#     initial: T,
# ):
#     iterator = iter(iterable)

#     def _accumulate(acc: T, iterator: Iterator[S]) -> ContinuationMonad[T]:
#         try:
#             value = next(iterator)
#         except StopIteration:
#             return from_value(acc)

#         def func1(n_acc):
#             def func2(_):
#                 return _accumulate(n_acc, iterator)

#             return schedule_trampoline().flat_map(func2)

#         # schedule on trampoline for stack safe recursive call
#         return func(acc, value).flat_map(func1)

#     return _accumulate(initial, iterator)


class defer[U]:
    def __new__(
        _,
        func: Callable[[Trampoline, DeferredObserver[U]], ContinuationCertificate],
    ):
        """
        Create a continuation monad that defers subscription until a source is specified via `connect`.

        This allows for lazy initialization of a subscription, where the actual source can be connected at a
        later time. The provided function must return a continuation certificate to ensure the continuation chain
        remains valid.

        Args:
            func: A function that receives a subscription object that can be stored for later connection, and
                must return a continuation certficat to maintain the monadic chain

        Returns:
            (ContinuationMonad[U]): A monad that will begin emitting elements once connected to a source


        ``` python
        subscriptions = [None]
        certificate = ...           # a valid continuation certificate

        def func(subscription):
            subscriptions[0] = subscription
            return certificate

        continuationmonad.defer(func)

        def later():
            # later, connect the stored subscription to a source
            continuationmonad.from_(None).continue_(subscriptions)
        ```
        """

        return init_continuation_monad(init_defer(func=func, stack=get_frame_summary()))


def zip[U](
    continuations: Iterable[ContinuationMonad[U]],
):
    return init_continuation_monad(init_zip(children=tuple(continuations)))


def from_[U](value: U):
    return init_continuation_monad(init_from_value(value=value))


def get_trampoline():
    return init_continuation_monad(init_get_trampoline())


def schedule_on(scheduler: Scheduler):
    return init_continuation_monad(init_schedule_on(scheduler=scheduler))


def schedule_trampoline():
    return get_trampoline().flat_map(
        lambda trampoline: schedule_on(scheduler=trampoline)
    )


def tail_rec(func: Callable[[], ContinuationMonad]):
    return schedule_trampoline().flat_map(lambda _: func())
