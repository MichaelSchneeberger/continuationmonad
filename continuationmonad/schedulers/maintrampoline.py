from typing import Callable
from continuationmonad.schedulers.continuation import Continuation
from continuationmonad.schedulers.trampoline import Trampoline


class MainTrampoline(Trampoline):
    def stop(self) -> Continuation:
        """
        The stop function is capable of creating the finishing Continuation
        """
        
        if self.is_stopped:
            raise Exception('Scheduler can only be stopped once.')

        self.is_stopped = True
        return self._create_continuation()

    def run(self, fn: Callable[[], Continuation]) -> None:
        super().run(fn=fn)


def init_main_trampoline():
    return MainTrampoline()
