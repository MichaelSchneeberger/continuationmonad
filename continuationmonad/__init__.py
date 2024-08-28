from continuationmonad.continuationmonad.from_ import (
    get_trampoline as _get_trampoline,
    from_value as _from_value,
    trampoline as _trampoline,
)
from continuationmonad.schedulers.continuation import (
    init_continuation as _init_continuation,
)
from continuationmonad.schedulers.maintrampoline import (
    init_main_trampoline as _init_main_trampoline,
)


init_continuation = _init_continuation
init_main_trampoline = _init_main_trampoline

get_trampoline = _get_trampoline
from_ = _from_value
trampoline = _trampoline
