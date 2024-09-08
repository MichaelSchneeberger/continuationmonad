from continuationmonad.cancellable import init_cancellable_leave as _init_cancellable
from continuationmonad.continuationmonad.from_ import (
    accumulate as _accumulate,
    defer as _defer,
    get_trampoline as _get_trampoline,
    from_value as _from_value,
    join as _join,
    schedule_on as _schedule_on,
    schedule_trampoline as _schedule_trampoline,
    tail_rec as _tail_rec,
)
from continuationmonad.continuationmonad.init import (
    init_continuation_monad as _init_continuation_monad,
)
from continuationmonad.continuationmonad.to import (
    fork as _fork,
)
from continuationmonad.schedulers.init import (
    init_main_trampoline as _init_main_trampoline,
    init_trampoline as _init_trampoline,
)


# Schedulers
############

init_cancellable = _init_cancellable
init_trampoline = _init_trampoline
init_main_trampoline = _init_main_trampoline


# Create continuation source
############################

from_ = _from_value
get_trampoline = _get_trampoline
schedule_trampoline = _schedule_trampoline
schedule_on = _schedule_on
tail_rec = _tail_rec


# Create continuation from others
#################################

accumulate = _accumulate
defer = _defer
join = _join


# Create a forked continuation
##############################

fork = _fork


# Implement your own operator
#############################

from_node = _init_continuation_monad
