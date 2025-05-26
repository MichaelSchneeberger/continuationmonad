from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.continuationmonadtree.subscribeargs import init_subscribe_args
from continuationmonad.scheduler.init import init_trampoline
from continuationmonad.scheduler.scheduler import Scheduler
from continuationmonad.testing.tobserver import TObserver


def test_run(
    source: ContinuationMonadNode,
    observer: TObserver,
    scheduler: Scheduler,
):
    trampoline = init_trampoline()

    def scheduler_task():
        def trampoline_task():
            certificate = source.subscribe(init_subscribe_args(
                observer=observer,
                trampoline=trampoline,
                weight=1,
                cancellation=None,
            ))
            return certificate

        return trampoline.start_loop(trampoline_task, weight=1, cancellation=None)
    observer.certificate = scheduler.schedule(scheduler_task, weight=1, cancellation=None)
