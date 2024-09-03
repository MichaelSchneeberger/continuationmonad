from continuationmonad.cancellable import init_cancellable_leave as _init_cancellable
from continuationmonad.continuationmonad.from_ import (
    get_trampoline as _get_trampoline,
    from_value as _from_value,
    schedule_on as _schedule_on,
    schedule_trampoline as _schedule_trampoline,
)
from continuationmonad.continuationmonad.init import (
    init_continuation_monad as _init_continuation_monad,
)
from continuationmonad.continuationmonad.from_ import (
    zip as _zip,
    accumulate as _accumulate,
)
from continuationmonad.continuationmonad.to import (
    fork as _fork,
)
from continuationmonad.deferredsubscriptionprovider import (
    init_deferred_subscription_provider as _init_deferred_subscription_provider,
)
from continuationmonad.schedulers.init import (
    init_main_trampoline as _init_main_trampoline,
    init_trampoline as _init_trampoline,
)


init_cancellable = _init_cancellable
init_trampoline = _init_trampoline
init_main_trampoline = _init_main_trampoline

from_node = _init_continuation_monad

# create continuation monad
###########################

schedule_on = _schedule_on
accumulate = _accumulate
zip = _zip

# operations
############

get_trampoline = _get_trampoline
from_ = _from_value
schedule_trampoline = _schedule_trampoline

fork = _fork

deferred_subscription_provider = _init_deferred_subscription_provider
