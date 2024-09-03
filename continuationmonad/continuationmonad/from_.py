from typing import Callable, Iterable, Iterator

from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.continuationmonad.init import init_continuation_monad
from continuationmonad.continuationmonadtree.init import init_get_trampoline, init_return, init_schedule_on, init_schedule_trampoline
from continuationmonad.schedulers.scheduler import Scheduler


def get_trampoline():
    return init_continuation_monad(child=init_get_trampoline())


def from_value[U](value: U):
    return init_continuation_monad(child=init_return(value=value))


def schedule_on(scheduler: Scheduler):
    return init_continuation_monad(init_schedule_on(scheduler=scheduler))


def schedule_trampoline():
    return init_continuation_monad(child=init_schedule_trampoline())


class zip[U]:
    def __new__(
        _, continuations: Iterable[ContinuationMonad[U]]
    ) -> ContinuationMonad[tuple[U, ...]]:
        continuations_iterator = iter(continuations)

        try:
            current = next(continuations_iterator).map(lambda v: (v,))
        except StopIteration:
            return from_value(tuple[U]())

        for other in continuations_iterator:
            current = other.flat_map(
                lambda v, current=current: current.map(lambda t: t + (v,))
            )

        return current


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
        print(value)

        def func1(n_acc):
            def func2(_):
                return _accumulate(n_acc, iterator)

            return schedule_trampoline().flat_map(func2)

        # schedule on trampoline for stack safe recursive call
        return func(acc, value).flat_map(func1)

    return _accumulate(initial, iterator)
