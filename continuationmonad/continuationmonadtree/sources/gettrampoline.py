from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode


class GetTrampoline(ContinuationMonadNode[Trampoline]):
    def __str__(self) -> str:
        return 'get_trampoline()'

    def subscribe(
        self,
        args: SubscribeArgs,
    ):
        return args.on_next(args.trampoline, args.trampoline)

        # def task():
        #     return args.on_next(args.trampoline, args.trampoline)

        # return args.trampoline.schedule(
        #     task=task, weight=args.weight, cancellation=args.cancellation
        # )
