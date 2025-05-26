from unittest import TestCase

from continuationmonad.scheduler.init import init_virtual_time_scheduler
from continuationmonad.continuationmonadtree.init import (
    init_error,
    init_flat_map,
    init_from_value,
)
from continuationmonad.testing.tobserver import init_test_observer
from continuationmonad.testing.trun import test_run


class TestFlatMap(TestCase):
    def test_normal_use_case(self):
        scheduler = init_virtual_time_scheduler()

        inner_source1 = init_from_value(1)

        observer = init_test_observer()

        test_run(
            source=init_flat_map(
                child=init_from_value(inner_source1),
                func=lambda c: c,
                stack=tuple(),
            ),
            observer=observer,
            scheduler=scheduler,
        )

        scheduler.advance_to(0.5)

        self.assertEqual(observer.received_item, 1)

    def test_inner_error_case(self):
        scheduler = init_virtual_time_scheduler()

        exception = Exception('TestException')
        inner_source1 = init_error(exception)

        observer = init_test_observer()

        test_run(
            source=init_flat_map(
                child=init_from_value(inner_source1),
                func=lambda c: c,
                stack=tuple(),
            ),
            observer=observer,
            scheduler=scheduler,
        )

        scheduler.advance_to(0.5)

        self.assertEqual(observer.received_exception, exception)
