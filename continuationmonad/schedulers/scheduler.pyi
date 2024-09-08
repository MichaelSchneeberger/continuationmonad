from abc import ABC, abstractmethod
from typing import Callable

from continuationmonad.cancellable import CertificateProvider
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate


class Scheduler(ABC):
    @abstractmethod
    def schedule(
        self,
        fn: Callable[[], ContinuationCertificate],
        certificate_provider: CertificateProvider | None = None,
    ) -> ContinuationCertificate: ...

    def _create_certificate(self) -> ContinuationCertificate: ...
