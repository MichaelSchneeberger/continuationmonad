from unittest import TestCase

from continuationmonad.continuationmonadtree.init import init_flat_map, init_from_value
from continuationmonad.continuationmonadtree.subscribeargs import init_subscribe_args
from continuationmonad.scheduler.init import init_main_scheduler, init_trampoline
from continuationmonad.testing.tobserver import init_test_observer


class TestFlatMap(TestCase):
    def test_1(self):
        inner_source1 = init_from_value(1)
        source = init_from_value(inner_source1)

        trampoline = init_trampoline()
        main_scheduler = init_main_scheduler()

        sink = init_test_observer(main_scheduler=main_scheduler)

        def schedule_task():
            def trampoline_task():
                certificate = init_flat_map(
                    child=source,
                    func=lambda v: v,
                    stack=tuple(),
                ).subscribe(init_subscribe_args(
                    observer=sink,
                    trampoline=trampoline,
                    weight=1,
                    cancellation=None,
                ))
                return certificate
        
            return trampoline.run(trampoline_task, weight=1)
        main_scheduler.run(schedule_task)

        self.assertEqual(sink.received, [1])
