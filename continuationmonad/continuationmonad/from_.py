from typing import Callable, Iterable, Iterator
import itertools

from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.continuationmonad.init import init_continuation_monad
from continuationmonad.continuationmonadtree.data.deferredsubscription import (
    DeferredSubscription,
)
from continuationmonad.continuationmonadtree.init import (
    init_defer_subscription,
    init_get_trampoline,
    init_join,
    init_return,
    init_schedule_on,
    init_schedule_trampoline,
)
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.schedulers.trampoline import Trampoline


def accumulate[S, T](
    func: Callable[[T, S], ContinuationMonad[T]],
    iterable: Iterable[S],
    initial: T,
):
    iterator = iter(iterable)

    def _accumulate(acc: T, iterator: Iterator[S]) -> ContinuationMonad[T]:
        try:
            value = next(iterator)
        except StopIteration:
            return from_value(acc)

        def func1(n_acc):
            def func2(_):
                return _accumulate(n_acc, iterator)

            return schedule_trampoline().flat_map(func2)

        # schedule on trampoline for stack safe recursive call
        return func(acc, value).flat_map(func1)

    return _accumulate(initial, iterator)


def defer[U](
    func: Callable[
        [DeferredSubscription[U]], ContinuationMonadNode[ContinuationCertificate]
    ],
):
    return init_continuation_monad(child=init_defer_subscription(func=func))


def join[U](
    continuations: Iterable[ContinuationMonad[U]],
):
    return init_continuation_monad(init_join(children=tuple(continuations)))


def from_value[U](value: U):
    return init_continuation_monad(child=init_return(value=value))


def get_trampoline():
    return init_continuation_monad(child=init_get_trampoline())


def schedule_on(scheduler: Scheduler):
    return init_continuation_monad(init_schedule_on(scheduler=scheduler))


def schedule_trampoline():
    return init_continuation_monad(child=init_schedule_trampoline())


def tail_rec[U](func: Callable[[], ContinuationMonad[U]]):
    return schedule_trampoline().flat_map(lambda _: func())
