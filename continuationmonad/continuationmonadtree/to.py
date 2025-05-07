from dataclasses import dataclass
from typing import Callable

from continuationmonad.scheduler.cancellation import Cancellation
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.instantscheduler import InstantScheduler
from continuationmonad.scheduler.mainschedulermixin import MainScheduler
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.scheduler.init import init_trampoline
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

    def on_success(self, _, item: ContinuationCertificate):
        return item

    def on_error(
        self, trampoline: Trampoline, exception: Exception
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

                return trampoline.run(
                    trampoline_task, weight=weight, cancellation=cancellation
                )

            return scheduler.schedule(
                task=schedule_task,
                weight=weight,
                cancellation=cancellation,
            )


def run[V](
    source: ContinuationMonadNode[V],
    scheduler: MainScheduler | None = None,
) -> V:
    if scheduler is None:
        main_scheduler = init_main_scheduler()
    else:
        main_scheduler = scheduler
    
    trampoline = init_trampoline()

    received_exception = []
    received_item = []

    class MainObserver(Observer):
        def on_success(self, _, item: V) -> ContinuationCertificate:
            received_item.append(item)
            return main_scheduler.stop()

        def on_error(self, _, exception: Exception) -> ContinuationCertificate:
            received_exception.append(exception)
            return main_scheduler.stop()

    args = init_subscribe_args(
        observer=MainObserver(),
        trampoline=trampoline,
        weight=1,
    )

    def schedule_task():
        def trampoline_task():
            return source.subscribe(args=args)

        return trampoline.run(trampoline_task, weight=1)

    main_scheduler.run(schedule_task)

    if received_exception:
        raise received_exception[0]

    return received_item[0]
