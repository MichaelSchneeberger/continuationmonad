from unittest import TestCase

from continuationmonad.scheduler.init import init_main_scheduler, init_trampoline
from continuationmonad.continuationmonadtree.subscribeargs import init_subscribe_args
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.continuationmonadtree.init import (
    init_error,
    init_flat_map,
    init_from_value,
)
from continuationmonad.testing.tobserver import init_test_observer


class TestFlatMap(TestCase):
    def setUp(self):
        self.trampoline = init_trampoline()
        self.main_scheduler = init_main_scheduler()
        self.sink = init_test_observer(main_scheduler=self.main_scheduler)

    def run_scheduler(self, source: ContinuationMonadNode):
        def schedule_task():
            def trampoline_task():
                certificate = init_flat_map(
                    child=source,
                    func=lambda v: v,
                    stack=tuple(),
                ).subscribe(
                    init_subscribe_args(
                        observer=self.sink,
                        trampoline=self.trampoline,
                        weight=1,
                        cancellation=None,
                    )
                )
                return certificate

            return self.trampoline.run(trampoline_task, weight=1)

        self.main_scheduler.run(schedule_task)

    def test_normal_use_case(self):
        inner_source1 = init_from_value(1)
        source = init_from_value(inner_source1)

        self.run_scheduler(source=source)

        self.assertEqual(self.sink.received_item, 1)

    def test_inner_error_case(self):
        exception = Exception()
        inner_source1 = init_error(exception)
        source = init_from_value(inner_source1)

        self.run_scheduler(source=source)

        self.assertEqual(self.sink.received_exception, exception)
