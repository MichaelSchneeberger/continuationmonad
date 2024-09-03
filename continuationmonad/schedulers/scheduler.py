from abc import abstractmethod
from typing import Callable

from continuationmonad.cancellable import CertificateProvider
from continuationmonad.lockmixin import LockMixin
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate


class Scheduler(LockMixin):
    @abstractmethod
    def schedule(
        self,
        fn: Callable[[], ContinuationCertificate],
        certificate_provider: CertificateProvider | None = None,
    ) -> ContinuationCertificate: ...

    @staticmethod
    def _create_continuation():
        _ContinuationCertificate = type(
            ContinuationCertificate.__name__,
            ContinuationCertificate.__mro__,
            ContinuationCertificate.__dict__ | {"__permission__": True},
        )
        return _ContinuationCertificate(lock=self.lock)
