from continuationmonad.scheduler.continuationcertificate import init_composite_continuation_certificate as _init_composite_continuation_certificate
from continuationmonad.scheduler.init import (
    init_current_thread_scheduler as _init_current_thread_scheduler,
    init_event_loop_scheduler as _init_event_loop_scheduler,
    init_main_scheduler as _init_main_scheduler,
    init_trampoline as _init_trampoline,
    init_main_trampoline as _init_main_trampoline,
    init_virtual_time_scheduler as _init_virtual_time_scheduler,
    init_main_virtual_time_scheduler as _init_main_virtual_time_scheduler,
    init_asyncio_scheduler as _init_asyncio_scheduler,
    init_main_asyncio_scheduler as _init_main_asyncio_scheduler
)
from continuationmonad.continuationmonadtree.subscribeargs import (
    init_subscribe_args as _init_subscribe_args,
)
from continuationmonad.continuationmonad.init import (
    init_continuation_monad as _init_continuation_monad,
)
from continuationmonad.continuationmonadtree.observer import (
    init_anonymous_observer as _init_anonymous_observer,
)
from continuationmonad.continuationmonad.from_ import (
    defer as _defer,
    decrease_weight as _decrease_weight,
    get_trampoline as _get_trampoline,
    error as _error,
    from_ as _from_value,
    increase_weight as _increase_weight,
    schedule_on as _schedule_on,
    schedule_relative as _schedule_relative,
    schedule_absolute as _schedule_absolute,
    schedule_trampoline as _schedule_trampoline,
    tail_rec as _tail_rec,
    zip as _zip,
)
from continuationmonad.continuationmonad.to import (
    fork as _fork,
    run as _run,
    to_asyncio as _to_asyncio,
)


init_composite_continuation_certificate = _init_composite_continuation_certificate


# Schedulers
############

init_current_thread_scheduler = _init_current_thread_scheduler
init_event_loop_scheduler = _init_event_loop_scheduler
init_main_scheduler = _init_main_scheduler
init_trampoline = _init_trampoline
init_main_trampoline = _init_main_trampoline
init_virtual_time_scheduler = _init_virtual_time_scheduler
init_main_virtual_time_scheduler = _init_main_virtual_time_scheduler
init_asyncio_scheduler = _init_asyncio_scheduler
init_main_asyncio_scheduler = _init_main_asyncio_scheduler


# Implement custom continuation monad
#####################################

init_subscribe_args = _init_subscribe_args
init_anonymous_observer = _init_anonymous_observer


# Create continuation source
############################

defer = _defer
decrease_weight = _decrease_weight
error = _error
from_ = _from_value
get_trampoline = _get_trampoline
increase_weight = _increase_weight
return_ = _from_value
schedule_trampoline = _schedule_trampoline
schedule_on = _schedule_on
sleep = _schedule_relative
delay = _schedule_relative
schedule_relative = _schedule_relative  # depricated
schedule_absolute = _schedule_absolute  # depricated
tail_rec = _tail_rec    # depricated


# Create continuation from others
#################################

# accumulate = _accumulate
zip = _zip


# Fork continuation monad on trampoline
#######################################

fork = _fork
create_task = _fork
run = _run
to_asyncio = _to_asyncio


# Implement your own operator
#############################

from_node = _init_continuation_monad
