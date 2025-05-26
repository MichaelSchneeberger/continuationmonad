from unittest import TestCase

from donotation import do

from continuationmonad.continuationmonad.from_ import from_, schedule_relative
from continuationmonad.continuationmonadtree.init import init_zip
from continuationmonad.scheduler.init import init_virtual_time_scheduler
from continuationmonad.testing.tobserver import init_test_observer
from continuationmonad.testing.trun import test_run


class TestZip(TestCase):
    def test_1(self):
        scheduler = init_virtual_time_scheduler()
        
        @do()
        def gen_source1():
            yield schedule_relative(1, scheduler)
            return from_(1)
        
        @do()
        def gen_source2():
            return from_(2)

        source1 = gen_source1()
        source2 = gen_source2()
        observer = init_test_observer()

        test_run(
            source=init_zip(
                children=(source1, source2),
            ),
            observer=observer,
            scheduler=scheduler,
        )

        scheduler.advance_to(1.5)

        self.assertEqual(observer.received_item, (1, 2))
