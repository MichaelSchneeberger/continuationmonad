from unittest import TestCase

from donotation import do

from continuationmonad.continuationmonad.from_ import from_, schedule_with_delay
from continuationmonad.continuationmonadtree.init import init_zip
from continuationmonad.continuationmonadtree.nodes import ContinuationMonadNode
from continuationmonad.continuationmonadtree.subscribeargs import init_subscribe_args
from continuationmonad.scheduler.init import init_trampoline, init_virtual_time_scheduler
from continuationmonad.testing.tobserver import init_test_observer


class TestZip(TestCase):
    def setUp(self):
        self.trampoline = init_trampoline()
        self.scheduler = init_virtual_time_scheduler(is_main=True)
        self.sink = init_test_observer(main_scheduler=self.scheduler)

    def run_scheduler(self, sources: tuple[ContinuationMonadNode, ...]): #, sink: Observer):
        def schedule_task():
            def trampoline_task():
                certificate = init_zip(
                    children=sources,
                ).subscribe(init_subscribe_args(
                    observer=self.sink,
                    trampoline=self.trampoline,
                    weight=1,
                    cancellation=None,
                ))
                return certificate
        
            return self.trampoline.run(trampoline_task, weight=1)
        self.scheduler.run(schedule_task)

    def test_1(self):
        
        @do()
        def gen_source1():
            yield schedule_with_delay(self.scheduler, 1)
            return from_(1)
        
        @do()
        def gen_source2():
            return from_(2)

        source1 = gen_source1()
        source2 = gen_source2()

        self.run_scheduler(sources=(source1, source2))

        self.scheduler.advance_to(1.5)

        self.assertEqual(self.sink.received_item, (1, 2))

    # def test_inner_error_case(self):
    #     exception = Exception()
    #     inner_source1 = init_error(exception)
    #     source = init_from_value(inner_source1)

    #     self.run(source=source)

    #     self.assertEqual(self.sink.received_exception, exception)
