from abc import abstractmethod

from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode


class FromValue[U](ContinuationMonadNode[U]):
    def __str__(self) -> str:
        return f"from_value({self.value})"

    @property
    @abstractmethod
    def value(self) -> U: ...

    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        return args.on_next(args.trampoline, self.value)

        # def trampoline_task():
        #     return args.on_next(args.trampoline, self.value)

        # return args.trampoline.schedule(
        #     task=trampoline_task,
        #     weight=args.weight,
        #     cancellation=args.cancellation,
        # )
