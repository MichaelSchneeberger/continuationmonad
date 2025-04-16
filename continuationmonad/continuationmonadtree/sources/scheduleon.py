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
        def schedule_item():
            if isinstance(self.scheduler, Trampoline):
                return args.on_next(self.scheduler, self.scheduler)

            else:
                trampoline = init_trampoline()

                def trampoline_item():
                    return args.on_next(trampoline, self.scheduler)

                return trampoline.run(
                    trampoline_item, weight=args.weight, cancellation=args.cancellation
                )

        return self.scheduler.schedule(
            task=schedule_item, weight=args.weight, cancellation=args.cancellation
        )
