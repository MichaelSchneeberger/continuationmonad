from dataclasses import dataclass
from continuationmonad.continuationmonadtree.observer import Observer
from continuationmonad.scheduler.continuationcertificate import ContinuationCertificate
from continuationmonad.scheduler.schedulers.mainscheduler import MainScheduler
from continuationmonad.scheduler.schedulers.trampoline import Trampoline


@dataclass
class TObserver[U](Observer[U]):
    received: list[U]
    main_scheduler: MainScheduler

    def on_success(self, trampoline: Trampoline, item: U) -> ContinuationCertificate:
        self.received.append(item)
        return self.main_scheduler.stop()

    def on_error(self, trampoline: Trampoline, exception: Exception) -> ContinuationCertificate:
        return self.main_scheduler.stop()


def init_test_observer(main_scheduler: MainScheduler):
    return TObserver(
        received=[],
        main_scheduler=main_scheduler,
    )
