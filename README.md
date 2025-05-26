# Continuation-Monad

**Continuation-Monad** is a Python library for stack-safe, asynchronous computation using continuation-passing style.  
It wraps callbacks in a continuation monad and leverages trampoline-based schedulers to guarantee deadlock-free execution without growing the call stack.


## Features

- **Trampoline-based execution**: Ensures stack-safety by evaluating recursive computations iteratively.
- **Continuation certificates**: Ensures the execution of a continuation monad completes, avoiding any continuation deadlock.
- **Flexible schedulers**: Explicitly control execution context via multiple scheduler types.
- **Composable monadic operations**: Enables clean, functional-style pipelines with `map`, `flat_map`, and more.


## Installation

You can install **Continuation-Monad** using pip:

```
pip install continuationmonad
```


## Example

The example below recursively counts down from 5 to 0, using a trampoline to avoid stack overflow:

``` python
import continuationmonad


def count_down(count: int):
    print(f'{count=}')

    if count == 0:
        return continuationmonad.from_(count)
    
    else:
        # schedule task on trampoline before doing a recursive call
        return continuationmonad.schedule_trampoline().flat_map(
            lambda _: count_down(count - 1)
        )

# Runs the continuation and returns 0
result = continuationmonad.run(
    count_down(5)
)
```


## Schedulers and Trampolines

The library includes several schedulers to manage execution contexts:

- **AsyncIO Scheduler**:  
    Either run an asyncio loop on a dedicated background thread.
    ``` python
    scheduler = continuationmonad.init_asyncio_scheduler()
    ```
    Or, run an event loop on the current thread. Blocks on run() until stop() is called.
    ``` python
    scheduler = continuationmonad.init_main_asyncio_scheduler()
    ```

- **Current Thread Scheduler**:  
    A scheduler that is initially idle and starts upon the first `schedule` method call.
    ``` python
    scheduler = continuationmonad.init_current_thread_scheduler()
    ```

- **Event Loop Scheduler**:
    Either run an event loop on a dedicated background thread.
    ``` python
    scheduler = continuationmonad.init_event_loop_scheduler()
    ```
    Or, run an event loop on the current thread. Blocks on run() until stop() is called.
    ``` python
    scheduler = continuationmonad.init_event_loop_scheduler()
    ```

- **Trampoline**:  
    Lightweight and synchronous. Implements only schedule() and executes tasks immediately in a loop until the queue is empty.
    ``` python
    scheduler = continuationmonad.init_trampoline()
    ```


## Operations

### Creating Continuation Monads

- `defer` - Creates a deferred continuation, activated upon subscription.  
    (See [defer example](examples/basic/deferexample.py))
- `from_` (or `return_`): Wraps a value in a continuation monad:
    ``` python
    c = continuationmonad.from_(5)
    ```
- `get_trampoline` - Retrieves the default trampoline scheduler:
    ``` python
    c = continuationmonad.get_trampoline()
    ```
- `schedule_on` - Schedules continuation execution on the given scheduler:
    ``` python
    c = continuationmonad.schedule_on(scheduler)
    ```
- `schedule_trampoline` - Schedules execution on the active trampoline:
    ``` python
    c = continuationmonad.schedule_trampoline()
    ```
- `sleep` (or `delay`) - Schedules continuation execution on the given scheduler after a relative time:
    ``` python
    c = continuationmonad.sleep(scheduler, 1)
    ```
<!-- - `tail_rec` - Performs recursive calls in a stack-safe manner using the trampoline. -->


### Transforming operators

- `connect` - Connects the continuation to one or more subscribers.  
    (See [defer example](examples/basic/deferexample.py))
- `flat_map` - Applies a function that returns a continuation and flattens the result.
- `map` - Transforms the emitted item using the provided function.

### Combining operators

- `zip` - Combines items from multiple continuations into a tuple.
    (See [zip example](examples/basic/zipexample.py))


### Output functions

- `fork` (or `create_task`) - Runs the continuation on a separate trampoline.
    (See [defer example](examples/basic/deferexample.py))
- `run` - Executes the continuation on a new trampoline and returns its result.
- `to_asyncio` - Converts a continuation monad to a *asyncio* future.
