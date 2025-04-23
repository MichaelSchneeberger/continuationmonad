from continuationmonad.scheduler.init import (
    init_current_thread_scheduler as _init_current_thread_scheduler,
    init_event_loop_scheduler as _init_event_loop_scheduler,
    init_main_scheduler as _init_main_scheduler,
    init_trampoline as _init_trampoline,
)
from continuationmonad.continuationmonadtree.subscribeargs import (
    init_subscribe_args as _init_subscribe_args,
)
from continuationmonad.continuationmonad.init import (
    init_continuation_monad as _init_continuation_monad,
)
from continuationmonad.continuationmonad.from_ import (
    defer as _defer,
    get_trampoline as _get_trampoline,
    from_ as _from_value,
    zip as _zip,
    schedule_on as _schedule_on,
    schedule_trampoline as _schedule_trampoline,
    tail_rec as _tail_rec,
)
from continuationmonad.continuationmonad.to import fork as _fork


init_subscribe_args = _init_subscribe_args


# Schedulers
############

init_current_thread_scheduler = _init_current_thread_scheduler
init_event_loop_scheduler = _init_event_loop_scheduler
init_main_scheduler = _init_main_scheduler
init_trampoline = _init_trampoline


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


# Fork continuation monad on trampoline
#######################################

fork = _fork


# Implement your own operator
#############################

from_node = _init_continuation_monad
