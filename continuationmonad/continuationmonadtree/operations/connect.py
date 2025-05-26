from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable, override

from continuationmonad.continuationmonadtree.deferredhandler import DeferredHandler
from continuationmonad.continuationmonadtree.observer import Observer
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import (
    SingleChildContinuationMonadNode,
)
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


@dataclass
class ConnectObserver[U](Observer[U]):
    observer: Observer[tuple[ContinuationCertificate, ...]]
    handlers: Iterable[DeferredHandler]

    @override
    def on_success(self, trampoline: Trampoline, weight: int, item: U):
        def gen_certificates():
            for handler in self.handlers:

                def request_next_item(handler=handler):
                    return handler.resume(trampoline, weight, item)

                yield trampoline.schedule(
                    task=request_next_item,
                    weight=handler.weight,
                    cancellation=None,      # todo: include cancellation
                )

        certificates = tuple(gen_certificates())

        return self.observer.on_success(trampoline, weight, certificates)

    @override
    def on_error(self, trampoline: Trampoline, weight: int, exception: Exception):
        return self.observer.on_error(trampoline, weight, exception)


class Connect[U](
    SingleChildContinuationMonadNode[U, tuple[ContinuationCertificate, ...]]
):
    def __str__(self) -> str:
        return f"connect({self.handlers})"

    @property
    @abstractmethod
    def handlers(self) -> Iterable[DeferredHandler]: ...

    @override
    def subscribe(
        self,
        args: SubscribeArgs[tuple[ContinuationCertificate, ...]],
    ) -> ContinuationCertificate:
        return self.child.subscribe(
            args=args.copy(
                observer=ConnectObserver[U](
                    observer=args.observer,
                    handlers=self.handlers,
                )
            )
        )

