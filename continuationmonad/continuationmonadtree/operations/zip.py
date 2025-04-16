from abc import ABC, abstractmethod
from typing import Callable
from dataclasses import dataclass
from threading import RLock

from continuationmonad.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import (
    MultiChildrenContinuationMonadNode,
)


class ZipState: ...


@dataclass
class WaitState(ZipState):
    counter: int


class OnNextState(ZipState): ...


class ZipAction(ABC):
    @abstractmethod
    def get_action(self) -> ZipState: ...

    @abstractmethod
    def get_values(self) -> tuple: ...


@dataclass
class BaseAction(ZipAction):
    counter: int

    def get_action(self):
        return WaitState(counter=self.counter)

    def get_values(self) -> tuple:
        return tuple()


@dataclass
class OnNextAction[U](ZipAction):
    child: ZipAction
    value: U

    def get_action(self):
        p_node = self.child.get_action()

        match p_node:
            case WaitState(counter=1):
                return OnNextState()
            case WaitState(counter=counter):
                return WaitState(counter=counter - 1)

    def get_values(self) -> tuple:
        return self.child.get_values() + (self.value,)


@dataclass
class OnNextZip[U]:
    state: ZipAction
    lock: RLock
    certificates: list[ContinuationCertificate]
    on_next: Callable[[Trampoline, tuple[U, ...]], ContinuationCertificate]

    def __call__(self, trampoline: Trampoline, value: U):
        node = OnNextAction(
            child=None,  # type: ignore
            value=value,
        )

        with self.lock:
            node.child = self.state
            self.state = node

        action = node.get_action()

        match action:
            case OnNextState():
                return self.on_next(trampoline, node.get_values())
            case _:
                return self.certificates.pop()


class Zip[U](MultiChildrenContinuationMonadNode[U, tuple[U, ...]]):
    def __str__(self) -> str:
        return f"zip({self.children})"

    def subscribe(
        self,
        args: SubscribeArgs,
    ) -> ContinuationCertificate:
        on_next = OnNextZip(
            state=BaseAction(counter=len(self.children)),
            lock=RLock(),
            certificates=None,  # type: ignore
            on_next=args.on_next,
        )
        args = args.copy(on_next=on_next)

        def gen_certificates():
            for child in self.children:

                def child_subscription(child=child):
                    return child.subscribe(args=args)

                yield args.trampoline.schedule(
                    child_subscription,
                    weight=args.weight,
                    cancellation=args.cancellation,
                )

        certificates_iter = gen_certificates()

        certificate = next(certificates_iter)

        # overwrite certificates attribute
        on_next.certificates = list(certificates_iter)

        return certificate
