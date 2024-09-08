from abc import ABC, abstractmethod
from typing import Callable
from dataclasses import dataclass
from threading import RLock

from continuationmonad.cancellable import CancellableLeave
from continuationmonad.continuationmonadtree.nodes import MultiChildrenContinuationMonadNode
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class JoinAction: ...


@dataclass
class WaitAction(JoinAction):
    counter: int


class OnNextAction(JoinAction): ...


class JoinState(ABC):
    @abstractmethod
    def get_action(self) -> JoinAction: ...

    @abstractmethod
    def get_values(self) -> tuple: ...



@dataclass
class BaseState(JoinState):
    counter: int

    def get_action(self):
        return WaitAction(counter=self.counter)
    
    def get_values(self) -> tuple:
        return tuple()


@dataclass
class OnNext[U](JoinState):
    child: JoinState
    value: U

    def get_action(self):
        p_node = self.child.get_action()

        match p_node:
            case WaitAction(counter=1):
                return OnNextAction()
            case WaitAction(counter=counter):
                return WaitAction(counter=counter - 1)
            
    def get_values(self) -> tuple:
        return self.child.get_values() + (self.value,)

@dataclass
class OnNextJoin[U]:
    state: JoinState
    lock: RLock
    certificates: list[ContinuationCertificate]
    on_next: Callable[[Trampoline, tuple[U, ...]], ContinuationCertificate]

    def __call__(self, trampoline: Trampoline, value: U):
        node = OnNext(
            child=None, # type: ignore
            value=value,
        )

        with self.lock:
            node.child = self.state
            self.state = node

        action = node.get_action()

        match action:
            case OnNextAction():
                return self.on_next(trampoline, node.get_values())
            case _:
                return self.certificates.pop()


class Join[U](MultiChildrenContinuationMonadNode[U, tuple[U, ...]]):
    def __str__(self) -> str:
        return 'join()'

    def subscribe(
        self,
        trampoline: Trampoline, 
        on_next: Callable[[Trampoline, tuple[U, ...]], ContinuationCertificate],
        cancellable: CancellableLeave | None = None,
    ) -> ContinuationCertificate:
        on_next = OnNextJoin(
            state=BaseState(counter=len(self.children)),
            lock=RLock(),
            certificates=None, # type: ignore
            on_next=on_next,
        )
        
        def gen_certificates():
            for child in self.children:
                def child_subscription(child=child):
                    return child.subscribe(trampoline, on_next, cancellable=cancellable)

                yield trampoline.schedule(child_subscription)

        certificates_iter = gen_certificates()

        certificate = next(certificates_iter)
        
        # overwrite certificates attribute
        on_next.certificates = list(certificates_iter)

        return certificate
