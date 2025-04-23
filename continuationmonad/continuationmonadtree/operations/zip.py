from abc import ABC, abstractmethod
from typing import Callable
from dataclasses import dataclass
from threading import RLock

from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.trampoline import Trampoline
from continuationmonad.continuationmonadtree.subscribeargs import SubscribeArgs
from continuationmonad.continuationmonadtree.nodes import (
    MultiChildrenContinuationMonadNode,
)


# States
########

class ZipState: ...


@dataclass
class WaitStateBase(ZipState):
    certificates: tuple[ContinuationCertificate, ...]


@dataclass
class InitState(WaitStateBase):
    pass


@dataclass
class WaitState(WaitStateBase):
    certificate: ContinuationCertificate


class OnNextState(ZipState): ...


# Transitions
#############

class ZipTransition(ABC):
    @abstractmethod
    def get_state(self) -> ZipState: ...

    @abstractmethod
    def get_values(self) -> tuple: ...


@dataclass
class InitTransition(ZipTransition):
    counter: int
    certificates: tuple[ContinuationCertificate, ...]

    def get_state(self):
        return InitState(
            certificates=self.certificates,
        )

    def get_values(self) -> tuple:
        return tuple()


@dataclass
class OnNextTransition[U](ZipTransition):
    child: ZipTransition
    value: U

    def get_state(self):
        match state := self.child.get_state():           
            case WaitStateBase(certificates=certificates):
                if certificates:
                    return WaitState(
                        certificate=certificates[0],
                        certificates=certificates[1:],
                    )
                else:
                    return OnNextState()
            
            case _:
                raise Exception(f'Unexpected state {state}')

    def get_values(self) -> tuple:
        return self.child.get_values() + (self.value,)


@dataclass
class ZipObserver[U]:
    action: ZipTransition
    lock: RLock
    certificates: list[ContinuationCertificate]
    on_next: Callable[[Trampoline, tuple[U, ...]], ContinuationCertificate]

    def __call__(self, trampoline: Trampoline, value: U):
        action = OnNextTransition(
            child=None,  # type: ignore
            value=value,
        )

        with self.lock:
            action.child = self.action
            self.action = action

        match state := action.get_state():
            case OnNextState():
                return self.on_next(trampoline, action.get_values())
            
            case WaitState(certificate=certificate):
                return certificate
            
            case _:
                raise Exception(f'Unexpected state {state}')


class Zip[U](MultiChildrenContinuationMonadNode[U, tuple[U, ...]]):
    def __str__(self) -> str:
        return f"zip({self.children})"

    def subscribe(
        self,
        args: SubscribeArgs,
    ) -> ContinuationCertificate:
        observer = ZipObserver(
            action=None,
            lock=RLock(),
            certificates=None,  # type: ignore
            on_next=args.on_next,
        )
        args = args.copy(on_next=observer)

        def gen_certificates():
            for child in self.children:
                def child_subscription(child=child):
                    return child.subscribe(args=args)

                yield args.trampoline.schedule(
                    child_subscription,
                    weight=args.weight,
                    cancellation=args.cancellation,
                )

        certificates = tuple(gen_certificates())

        observer.action = InitTransition(
            counter=len(self.children),
            certificates=certificates[1:],
        )

        return certificates[0]
