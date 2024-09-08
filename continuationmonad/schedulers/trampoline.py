from __future__ import annotations

from collections import deque
from threading import RLock
from typing import Callable, Deque, override
from continuationmonad.cancellable import CertificateProvider
from continuationmonad.exceptions import ContinuationMonadSchedulerException
from continuationmonad.schedulers.data.continuationcertificate import ContinuationCertificate
from continuationmonad.schedulers.scheduler import Scheduler


class Trampoline(Scheduler):
    def __init__(self):
        self.is_stopped = False
        self._queue: Deque[tuple[Callable, CertificateProvider | None]] = deque()
        self._lock = RLock()

    @property
    def lock(self) -> RLock:
        return self._lock

    @override
    def schedule(
        self,
        fn: Callable[[], ContinuationCertificate],
        certificate_provider: CertificateProvider | None = None,
    ) -> ContinuationCertificate:
        # if self.is_stopped and len(self._queue) == 0:
        #     raise Exception('Scheduler is stopped, no functions can be scheduled.')

        self._queue.append((fn, certificate_provider))
        return self._create_certificate()

    def run(
        self,
        fn: Callable[[], ContinuationCertificate],
        certificate_provider: CertificateProvider | None = None,
    ) -> ContinuationCertificate:
        certificate = self.schedule(fn, certificate_provider)

        while self._queue:
            queued_fn, queued_cancellable = self._queue.popleft()

            if queued_cancellable and (certificate := queued_cancellable.get_certificate()):
                pass

            else:
                # call scheduled function
                certificate = queued_fn()

            try:
                # verify that the continuation is used once
                verified = certificate.verify()

            except Exception:
                raise ContinuationMonadSchedulerException(
                    f'Certificate returned by {queued_fn} could not be verified.'
                )
            
            if not verified:
                raise ContinuationMonadSchedulerException(
                    f'Certificate {certificate} has already been verified.'
                )

        self.is_stopped = True
        return certificate
