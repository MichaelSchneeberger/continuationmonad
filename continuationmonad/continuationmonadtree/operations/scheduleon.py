from abc import abstractmethod
from typing import Callable

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.init import init_trampoline
from continuationmonad.schedulers.scheduler import Scheduler
from continuationmonad.schedulers.trampoline import Trampoline



class ScheduleOn(ContinuationMonadNode[None]):
    def __str__(self) -> str:
        return f'schedule_on({self.scheduler})'

    @property
    @abstractmethod
    def scheduler(self) -> Scheduler:
        ...

    def subscribe(
        self,
        _, 
        on_next: Callable[[Trampoline, None], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate:
        def schedule_item():
            if isinstance(self.scheduler, Trampoline):
                return on_next(self.scheduler, None)

            else:
                trampoline = init_trampoline()

                def trampoline_item():
                    return on_next(trampoline, None)
                
                return trampoline.run(trampoline_item, cancellable)
        return self.scheduler.schedule(schedule_item, cancellable)