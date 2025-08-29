from __future__ import annotations
from abc import abstractmethod
from dataclasses import replace
from functools import cached_property
from threading import Lock
from typing import override

from dataclassabc import dataclassabc

from continuationmonad.exceptions import ContinuationMonadOperatorException
from continuationmonad.utils.framesummary import (
    FrameSummaryMixin,
    FrameSummary,
    get_frame_summary,
)


class ContinuationCertificateMixin(FrameSummaryMixin):
    def __repr__(self):
        return f"{self.__class__.__name__}(weight={self.weight}, velidated={self.validated})"

    @property
    @abstractmethod
    def weight(self) -> int:
        """virtual multiplicity of a task execution"""
        ...

    @property
    @abstractmethod
    def validated(self) -> bool: ...

    @property
    @abstractmethod
    def lock(self) -> Lock: ...

    @abstractmethod
    def validate(self, weight: int): ...

    def or_(self, other: ContinuationCertificate):
        if not self.validated:
            return self
        else:
            return other

    def split(
        self, partition: tuple[int, ...], stack: tuple[FrameSummary, ...] | None = None
    ):
        assert sum(partition) == self.weight

        if stack is None:
            stack = get_frame_summary()

        self.validate(self.weight)

        def gen_certificates():
            for weight in partition:
                yield ContinuationCertificate(
                    lock=self.lock,
                    weight=weight,
                    stack=stack,
                    validated=False,
                )

        return tuple(gen_certificates())

    def take(
        self,
        weight: int,
        stack: tuple[FrameSummary, ...] | None = None,
    ):
        if stack is None:
            stack = get_frame_summary()

        if self.weight < weight:
            traceback_msg = self.to_operator_traceback(stack=self.stack)
            raise ContinuationMonadOperatorException(
                f"The Weight {weight} to take it larger than {self.weight}\n{traceback_msg}"
            )

        return self.split(
            partition=(weight, self.weight - weight),
            stack=stack,
        )

    @staticmethod
    def merge(
        certificates: tuple[ContinuationCertificate, ...],
        stack: tuple[FrameSummary, ...] | None = None,
    ):
        if stack is None:
            stack = get_frame_summary()

        first, *_ = certificates

        def gen_weight():
            for certificate in certificates:
                weight = certificate.weight
                certificate.validate(weight)
                yield weight

        total_weight = sum(gen_weight())

        certificate = ContinuationCertificate(
            lock=first.lock,
            weight=total_weight,
            stack=stack,
            validated=False,
        )
        return certificate


@dataclassabc(repr=False)
class ContinuationCertificate(ContinuationCertificateMixin):
    lock: Lock
    weight: int
    stack: tuple[FrameSummary, ...]
    validated: bool

    # def copy(
    #     self, /,
    #     weight: int | None = None,
    #     stack: tuple[FrameSummary, ...] | None = None,
    # ):
    #     def gen_args():
    #         if weight is not None:
    #             yield 'weight', weight
    #         if stack is not None:
    #             yield 'stack', stack

    #     return replace(self, **dict(gen_args()))

    @override
    def validate(self, weight: int):
        """
        A continuation can be verified exactly once.
        """

        if weight != self.weight:
            traceback_msg = self.to_operator_traceback(stack=self.stack)
            raise ContinuationMonadOperatorException(
                f"The provided weight {weight} does not match the certificate weight {self.weight}."
                f"\n{traceback_msg}"
            )

        with self.lock:
            p_verified = self.validated
            self.validated = True

        if p_verified:
            traceback_msg = self.to_operator_traceback(stack=self.stack)
            raise ContinuationMonadOperatorException(
                f"The certificate has already been verified.\n{traceback_msg}"
            )


@dataclassabc(repr=False)
class CompositeContinuationCertificate(ContinuationCertificateMixin):
    underlying: tuple[ContinuationCertificateMixin, ...]
    stack: tuple[FrameSummary, ...]
    lock: Lock

    @cached_property
    def weight(self):
        def gen_weights():
            for c in self.underlying:
                yield c.weight

        return sum(gen_weights())

    @cached_property
    def validated(self):
        def gen_validated():
            for c in self.underlying:
                yield c.validated

        return any(gen_validated())

    @override
    def validate(self, weight: int):
        if weight != self.weight:
            traceback_msg = self.to_operator_traceback(stack=self.stack)
            raise ContinuationMonadOperatorException(
                f"The provided weight {weight} does not match the certificate weight {self.weight}."
                f"\n{traceback_msg}"
            )

        for c in self.underlying:
            c.validate(c.weight)


def init_composite_continuation_certificate(
    underlying: tuple[ContinuationCertificateMixin, ...],
    stack: tuple[FrameSummary, ...] | None = None,
):
    if stack is None:
        stack = get_frame_summary()

    return CompositeContinuationCertificate(
        underlying=underlying,
        stack=stack,
        lock=underlying[0].lock,
    )
