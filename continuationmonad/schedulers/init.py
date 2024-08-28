

from continuationmonad.schedulers.maintrampoline import MainTrampoline
from continuationmonad.schedulers.trampoline import Trampoline


def init_main_trampoline():
    return MainTrampoline()


def init_trampoline():
    return Trampoline()
