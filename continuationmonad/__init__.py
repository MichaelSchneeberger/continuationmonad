# from continuationmonad.schedulers.data.cancellable import (
#     init_cancellation_state as _init_cancellable,
# )
from continuationmonad.schedulers.init import (
    init_main_trampoline as _init_main_trampoline,
    # init_trampoline as _init_trampoline,
)
from continuationmonad.continuationmonadtree.subscribeargs import (
    init_subscribe_args as _init_subscribe_args,
)
from continuationmonad.continuationmonad.init import (
    init_continuation_monad as _init_continuation_monad,
)
from continuationmonad.continuationmonad.from_ import (
    # accumulate as _accumulate,
    defer as _defer,
    get_trampoline as _get_trampoline,
    from_ as _from_value,
    zip as _zip,
    schedule_on as _schedule_on,
    schedule_trampoline as _schedule_trampoline,
    tail_rec as _tail_rec,
)

init_subscribe_args = _init_subscribe_args


# Schedulers
############

init_trampoline = _init_main_trampoline
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

# accumulate = _accumulate
defer = _defer
zip = _zip


# Implement your own operator
#############################

from_node = _init_continuation_monad
