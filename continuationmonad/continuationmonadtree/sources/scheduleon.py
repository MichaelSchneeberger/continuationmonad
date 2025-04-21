from abc import abstractmethod

from continuationmonad.schedulers.init import init_trampoline
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode


class ScheduleOn(ContinuationMonadNode[None]):
    def __str__(self) -> str:
        return f"schedule_on({self.scheduler})"

    @property
    @abstractmethod
    def scheduler(self) -> Scheduler: ...

    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        match self.scheduler:
            case Trampoline() as trampoline:
                def trampoline_task():
                    return args.on_next(trampoline, trampoline)
                
                return trampoline.schedule(
                    task=trampoline_task, weight=args.weight, cancellation=args.cancellation
                )

            case _:
                def schedule_task():
                    trampoline = init_trampoline()

                    return trampoline.run(
                        trampoline_task, weight=args.weight, cancellation=args.cancellation
                    )

                return self.scheduler.schedule(
                    task=schedule_task, weight=args.weight, cancellation=args.cancellation
                )
