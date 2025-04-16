# Continuation-Monad

A Python library that encapsulates callback functions within a continuation monad, utilizing a trampoline scheduler to enable stack-safe computations.


## Installation

You can install Continuation-Monad using pip:

```
pip install continuationmonad
```


## Example

``` python
import continuationmonad


def count_down(count: int):
    print(f'{count=}')

    if count == 0:
        return continuationmonad.from_(count)
    
    else:
        # schedule recursive call on the trampoline
        return continuationmonad.tail_rec(lambda: count_down(count - 1))

# runs continuation and returns 0
result = count_down(5).run()
```

