from typing import Callable
from continuationmonad.cancellable import CertificateProvider
from continuationmonad.schedulers.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.trampoline import Trampoline


class MainTrampoline(Trampoline):
    def stop(self) -> ContinuationCertificate:
        """
        The stop function is capable of creating the finishing Continuation
        """

        if self.is_stopped:
            raise Exception("Scheduler can only be stopped once.")

        self.is_stopped = True
        return self._create_continuation()

    def run(
        self,
        fn: Callable[[], ContinuationCertificate],
        certificate_provider: CertificateProvider | None = None,
    ) -> None:
        super().run(
            fn=fn, 
            certificate_provider=certificate_provider,
        )
