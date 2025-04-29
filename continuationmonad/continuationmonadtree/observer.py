from abc import ABC, abstractmethod
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


class Observer[V](ABC):
    @abstractmethod
    def on_success(
        self,
        trampoline: Trampoline,
        item: V,
    ) -> ContinuationCertificate: ...
    @abstractmethod
    def on_error(
        self,
        exception: Exception,
    ) -> ContinuationCertificate: ...
