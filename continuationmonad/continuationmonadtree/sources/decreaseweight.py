from abc import abstractmethod

from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode


class DecreaseWeight(ContinuationMonadNode[None]):
    def __str__(self) -> str:
        return f"decrease_weight({self.certificates})"

    @property
    @abstractmethod
    def certificates(self) -> tuple[ContinuationCertificate, ...]: ...

    def subscribe(
        self,
        args: SubscribeArgs[None],
    ):
        weight = args.weight - sum(c.weight for c in self.certificates)

        def trampoline_task():
            return args.observer.on_success(args.trampoline, weight, None)

        certificate = args.trampoline.schedule(
            task=trampoline_task,
            weight=weight,
            cancellation=args.cancellation,
        )

        return ContinuationCertificate.merge((certificate,) + self.certificates)
