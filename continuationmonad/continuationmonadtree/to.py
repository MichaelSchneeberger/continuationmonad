from dataclasses import dataclass
from typing import Callable, override

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.instantscheduler import InstantScheduler
from continuationmonad.scheduler.mainschedulermixin import MainSchedulerMixin
from continuationmonad.scheduler.schedulers.asyncioscheduler import AsyncIOScheduler
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.scheduler.init import init_main_scheduler, init_trampoline
from continuationmonad.continuationmonadtree.subscribeargs import init_subscribe_args
from continuationmonad.continuationmonadtree.observer import (
    Observer,
    init_anonymous_observer,
)
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode



@dataclass
class ForkObserver(Observer[ContinuationCertificate]):
    on_error_func: Callable[[Exception], ContinuationMonadNode[ContinuationCertificate]]
    cancellation: Cancellation | None
    weight: int

    def on_success(self, trampoline, weight, item: ContinuationCertificate):
        return item

    def on_error(
        self, trampoline: Trampoline, weight, exception: Exception
    ) -> ContinuationCertificate:
        args = init_subscribe_args(
            observer=init_anonymous_observer(
                on_success=lambda _, c: c,
            ),
            trampoline=trampoline,
            cancellation=self.cancellation,
            weight=self.weight,
        )

        return self.on_error_func(exception).subscribe(
            args=args,
        )


def fork(
    source: ContinuationMonadNode[ContinuationCertificate],
    on_error: Callable[[Exception], ContinuationMonadNode[ContinuationCertificate]],
    scheduler: InstantScheduler,
    weight: int,
    cancellation: Cancellation | None = None,
) -> ContinuationCertificate:
    match scheduler:
        case Trampoline() as trampoline:
            args = init_subscribe_args(
                observer=ForkObserver(
                    on_error_func=on_error,
                    cancellation=cancellation,
                    weight=weight,
                ),
                trampoline=trampoline,
                cancellation=cancellation,
                weight=weight,
            )

            def trampoline_task():
                return source.subscribe(args=args)

            return trampoline.schedule(
                trampoline_task,
                weight=weight,
                cancellation=cancellation,
            )

        case _:

            def schedule_task():
                trampoline = init_trampoline()

                args = init_subscribe_args(
                    observer=ForkObserver(
                        on_error_func=on_error,
                        cancellation=cancellation,
                        weight=weight,
                    ),
                    trampoline=trampoline,
                    cancellation=cancellation,
                    weight=weight,
                )

                def trampoline_task():
                    return source.subscribe(args=args)

                return trampoline.start_loop(
                    trampoline_task, weight=weight, cancellation=cancellation
                )

            return scheduler.schedule(
                task=schedule_task,
                weight=weight,
                cancellation=cancellation,
            )


def to_asyncio[U](
    source: ContinuationMonadNode[U],
    scheduler: AsyncIOScheduler,
):
    future = scheduler.loop.create_future()

    @dataclass
    class ToAsyncIOObserver(Observer):
        certificate: ContinuationCertificate

        def on_success(self, trampoline: Trampoline, item: U) -> ContinuationCertificate:
            future.set_result(item)
            return self.certificate

        def on_error(self, trampoline: Trampoline, exception: Exception) -> ContinuationCertificate:
            future.set_exception(exception)
            return self.certificate

    observer = ToAsyncIOObserver(certificate=None) # type: ignore

    class ToAsyncIOCancellation(Cancellation):
        @override
        def is_cancelled(self):
            if future.cancelled():
                return observer.certificate
        
    cancellation = ToAsyncIOCancellation()

    def scheduler_task():
        trampoline = init_trampoline()

        def trampoline_task():
            return source.subscribe(
                args=init_subscribe_args(
                    observer=observer,
                    trampoline=trampoline,
                    weight=1,
                )
            )

        return trampoline.start_loop(task=trampoline_task, weight=1, cancellation=cancellation)
    observer.certificate = scheduler.schedule(scheduler_task, weight=1, cancellation=cancellation)

    return future


def run[U](
    source: ContinuationMonadNode[U],
    scheduler: MainSchedulerMixin | None = None,
) -> U:
    if scheduler is None:
        main_scheduler = init_main_scheduler()
    else:
        main_scheduler = scheduler
    
    trampoline = init_trampoline()

    received_exception = []
    received_item = []

    class MainObserver(Observer):
        def on_success(self, trampoline, weight, item: U) -> ContinuationCertificate:
            received_item.append(item)
            return main_scheduler.stop(weight=weight)

        def on_error(self, trampoline, weight, exception: Exception) -> ContinuationCertificate:
            received_exception.append(exception)
            return main_scheduler.stop(weight=weight)

    args = init_subscribe_args(
        observer=MainObserver(),
        trampoline=trampoline,
        weight=1,
    )

    def schedule_task():
        def trampoline_task():
            return source.subscribe(args=args)

        return trampoline.start_loop(trampoline_task, weight=1, cancellation=None)

    main_scheduler.run(schedule_task, weight=1)

    if received_exception:
        raise received_exception[0]

    return received_item[0]
