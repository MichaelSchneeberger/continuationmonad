from donotation import do

import continuationmonad
from continuationmonad.typing import DeferredHandler, ContinuationCertificate

deferred_handlers: list[DeferredHandler] = [None]  # type: ignore
certificates: list[ContinuationCertificate] = [None] # type: ignore

def func(_, handler: DeferredHandler):
    deferred_handlers[0] = handler
    return certificates[0]

@do()
def defer_and_connect():
    trampoline = yield continuationmonad.get_trampoline()

    def on_error(exception: Exception):
        raise exception

    certificates[0] = continuationmonad.fork(
        source = (
            continuationmonad.from_(None)
            .flat_map(lambda _: continuationmonad.from_('defer').connect(deferred_handlers))
            .map(lambda cs: cs[0])
        ),
        on_error=on_error,
        scheduler=trampoline,
        weight=1,
    )

    return continuationmonad.defer(func)

result = continuationmonad.run(defer_and_connect())
print(result)
