from abc import abstractmethod

from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode


class IncreaseWeight(ContinuationMonadNode[ContinuationCertificate]):
    def __str__(self) -> str:
        return f"increase_weight({self.increase})"

    @property
    @abstractmethod
    def increase(self) -> int: ...

    def subscribe(
        self,
        args: SubscribeArgs[ContinuationCertificate],
    ):
        weight = args.weight + self.increase

        certificate_increase: list[ContinuationCertificate] = [None] # type: ignore

        def trampoline_task():
            return args.observer.on_success(args.trampoline, weight, certificate_increase[0])

        certificate = args.trampoline.schedule(
            task=trampoline_task,
            weight=weight,
            cancellation=args.cancellation,
        )

        certificate_increase[0], right = certificate.take(self.increase)

        return right
