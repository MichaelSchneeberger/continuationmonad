from donotation import do

import continuationmonad
from continuationmonad.typing import DeferredObserver, ContinuationCertificate

deferred_observers: list[DeferredObserver] = [None]  # type: ignore
certificates: list[ContinuationCertificate] = [None] # type: ignore

def func(_, observer: DeferredObserver):
    deferred_observers[0] = observer
    return certificates[0]

@do()
def defer_and_connect():
    trampoline = yield continuationmonad.get_trampoline()

    certificates[0] = continuationmonad.fork(
        source = (
            continuationmonad.from_(None)
            .flat_map(lambda _: continuationmonad.from_('defer').connect(deferred_observers))
            .map(lambda cs: cs[0])
        ),
        scheduler=trampoline,
        weight=1,
    )

    return continuationmonad.defer(func)

result = defer_and_connect().run()
print(result)
