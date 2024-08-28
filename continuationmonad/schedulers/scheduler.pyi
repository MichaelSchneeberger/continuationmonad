from abc import ABC, abstractmethod
from typing import Callable

from continuationmonad.schedulers.continuation import Continuation


class Scheduler(ABC):
    @abstractmethod
    def schedule(
        self,
        fn: Callable[[], Continuation],
    ) -> Continuation: ...

    def _create_continuation(self) -> Continuation: ...