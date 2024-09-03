from abc import ABC, abstractmethod
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate


class Cancellable(ABC):
    # def __init__(self):
    #     self.certificate = None

    @abstractmethod
    def cancel(self, certificate: ContinuationCertificate):
        # self.cancelled = certificate
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
