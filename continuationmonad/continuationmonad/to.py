from continuationmonad.cancellation import Cancellation
from continuationmonad.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.init import init_trampoline
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import init_subscribe_args
from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad


def fork(
    source: ContinuationMonad[ContinuationCertificate],
    scheduler: Scheduler,
    weight: int,
    cancellation: Cancellation | None = None,
) -> ContinuationCertificate:
    
    match scheduler:
        case Trampoline() as trampoline:
            args = init_subscribe_args(
                on_next=lambda _, c: c,
                trampoline=trampoline,
                cancellation=cancellation,
                weight=weight,
            )

            def trampoline_task():
                return source.subscribe(args=args)

            return trampoline.schedule(
                trampoline_task, weight=weight, cancellation=cancellation,
            )
        
        case _:
            def schedule_task():
                trampoline = init_trampoline()

                args = init_subscribe_args(
                    on_next=lambda _, c: c,
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
                task=schedule_task, weight=weight, cancellation=cancellation,
            )
