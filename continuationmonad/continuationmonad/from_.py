from continuationmonad.continuationmonad.init import init_continuation_monad
from continuationmonad.continuationmonadtree.init import init_get_trampoline, init_return, init_trampoline


def get_trampoline():
    return init_continuation_monad(child=init_get_trampoline())


def from_value[U](value: U):
    return init_continuation_monad(child=init_return(value=value))


def trampoline():
    return init_continuation_monad(child=init_trampoline())
