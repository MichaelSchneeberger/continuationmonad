from abc import ABC, abstractmethod
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate


class Cancellable(ABC):
    @abstractmethod
    def cancel(self, certificate: ContinuationCertificate):
        ...


class CertificateProvider(ABC):
    @abstractmethod
    def get_certificate(self) -> ContinuationCertificate | None:
        ...


class CancellableLeave(Cancellable, CertificateProvider):
    def __init__(self):
        self._certificate = None

    def cancel(self, certificate: ContinuationCertificate):
        self._cancelled = certificate

    def get_certificate(self) -> ContinuationCertificate | None:
        return self._certificate


def init_cancellable_leave():
    return CancellableLeave()
