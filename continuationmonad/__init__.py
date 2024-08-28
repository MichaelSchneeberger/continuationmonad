from typing import Iterable
from continuationmonad.continuationmonad.continuationmonad import ContinuationMonad
from continuationmonad.continuationmonad.from_ import (
    get_trampoline as _get_trampoline,
    from_value as _from_value,
    trampoline as _trampoline,
)
from continuationmonad.continuationmonad.init import (
    init_continuation_monad as _init_continuation_monad,
)
from continuationmonad.schedulers.continuation import (
    init_continuation as _init_continuation,
)
from continuationmonad.schedulers.init import (
    init_main_trampoline as _init_main_trampoline,
    init_trampoline as _init_trampoline,
)


init_continuation = _init_continuation
init_trampoline = _init_trampoline
init_main_trampoline = _init_main_trampoline

from_node = _init_continuation_monad

# operations
############

get_trampoline = _get_trampoline
from_ = _from_value
trampoline = _trampoline


class zip[U]:
    def __new__(_, continuations: Iterable[ContinuationMonad]):
        continuations_iterator = iter(continuations)

        try:
            current = next(continuations_iterator).map(lambda v: (v,))
        except StopIteration:
            return from_(tuple[U]())

        for other in continuations_iterator:
            current = other.flat_map(lambda v, current=current: current.map(lambda t: t + (v,)))
            
        return current
