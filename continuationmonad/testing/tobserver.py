from dataclasses import dataclass

from continuationmonad.continuationmonadtree.observer import Observer
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate


@dataclass(frozen=False)
class TObserver[U](Observer[U]):
    received_item: U | None
    received_exception: Exception | None
    certificate: ContinuationCertificate

    def on_success(self, trampoline, weight, item: U):
        self.received_item = item
        return self.certificate

    def on_error(self, trampoline, weight, exception: Exception):
        self.received_exception = exception
        return self.certificate


def init_test_observer(): #main_scheduler: MainSchedulerMixin):
    return TObserver(
        received_item=None,
        received_exception=None,
        certificate=None, # type: ignore
    )
