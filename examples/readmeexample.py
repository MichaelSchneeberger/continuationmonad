from donotation import do

import continuationmonad


@do()
def tail_recursion(count: int):
    print(f'{count=}')

    if count == 0:
        return continuationmonad.return_(count)
    
    else:
        # schedule recursive call on the trampoline
        yield from continuationmonad.trampoline()
        return tail_recursion(count - 1)

trampoline = continuationmonad.init_main_trampoline()

def action():
    def on_next(_, value: int):
        print(value)
        return trampoline.stop()

    cont = tail_recursion(5)
    return cont.subscribe(trampoline, on_next)

trampoline.run(action)
