from abc import ABC, abstractmethod
from typing import Callable
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


class Observer[U](ABC):
    @abstractmethod
    def on_success(
        self,
        trampoline: Trampoline,
        weight: int,
        item: U,
    ) -> ContinuationCertificate:
        """
        Args:
            trampoline: active trampline associated with the current task execution
            weight: virtual multiplicity of a task execution
            item: result of the task execution
        """
        ...

    @abstractmethod
    def on_error(
        self,
        trampoline: Trampoline,
        weight: int,
        exception: Exception,
    ) -> ContinuationCertificate: ...


class init_anonymous_observer[U]:
    def __new__(
        cls,
        on_success: Callable[[Trampoline, int, U], ContinuationCertificate],
        on_error: Callable[[Trampoline, int, Exception], ContinuationCertificate]
        | None = None,
    ):
        if on_error is None:

            def on_error_func(
                trampoline, weight, exception: Exception
            ) -> ContinuationCertificate:
                raise exception
        else:
            on_error_func = on_error

        class AnonymousObserver(Observer):
            def on_success(
                self, trampoline: Trampoline, weight: int, item: U
            ) -> ContinuationCertificate:
                return on_success(trampoline, weight, item)

            def on_error(
                self, trampoline: Trampoline, weight: int, exception: Exception
            ) -> ContinuationCertificate:
                return on_error_func(trampoline, weight, exception)

        return AnonymousObserver()
