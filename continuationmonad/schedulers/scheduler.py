from abc import abstractmethod
from threading import RLock
from typing import Callable

from continuationmonad.cancellable import CertificateProvider
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate


class Scheduler:
    @property
    @abstractmethod
    def lock(self) -> RLock: ...

    @abstractmethod
    def schedule(
        self,
        fn: Callable[[], ContinuationCertificate],
        certificate_provider: CertificateProvider | None = None,
    ) -> ContinuationCertificate: ...

    def _create_certificate(self):
        _ContinuationCertificate = type(
            ContinuationCertificate.__name__,
            ContinuationCertificate.__mro__,
            ContinuationCertificate.__dict__ | {"__permission__": True},
        )
        return _ContinuationCertificate(lock=self.lock)
