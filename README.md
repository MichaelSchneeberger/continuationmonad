# Continuation-Monad

A Python library implementing stack-safe continuations based on schedulers, ensuring deadlock-free asynchronous computations.
<!-- that encapsulates callback functions within a continuation monad, utilizing a trampoline scheduler to enable stack-safe computations. -->


## Features

* **Trampoline-based**: Stack-safe execution of the continuation monad through trampolining
* **Continuation certificate**: The execution of the continuation monad is guaranteed to finish, which introduces a small computational overhead
* **Scheduler-based**: Explicit control over execution context through different scheduler implementations
* **Composable operations**: Monadic operators for clean functional pipelines


## Installation

You can install **Continuation-Monad** using pip:

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

## Schedulers and Trampolines

A `Scheduler` is an abstract base class (ABC) that defines the core execution interface for managing continuations.
It defines an abstract `schedule` method that enqueues a task for execution.
To prevent continuation deadlocks, the scheduled task must return a *continuation certificate*, which can only be obtained by scheduling another task.
``` python
class Scheduler:
    def schedule(
        self,
        task: Callable[[], ContinuationCertificate],
        weight: int,
    ) -> ContinuationCertificate: ...
```

A `Trampoline` is a concrete implementation of a scheduler. 
It uses a simple while loop to process tasks until its internal queue is exhausted.
Continuations run within a dedicated Trampoline, that can be accessed using the `get_trampline` operator.
When using the `schedule_on` method, a Trampoline is nested within another scheduler.


### Continuation Certificates

Scheduling continuations across multiple threads can lead to continuation deadlocks, where a continuation never produces a result.
These deadlocks are particularly difficult to debug when the continuation chain includes third-party operators that may be poorly tested or unpredictable.
To mitigate this, the system enforces the use of *continuation certificates* when scheduling tasks.
A continuation certificate:
- Must be returned by a scheduled task
- Implements a `verify` method that can be called exactly once
- Can only be created by invoking the `schedule` method of a scheduler

This design guarantees that the only way to complete a scheduled task is by scheduling another task—ensuring progress and avoiding deadlocks by construction.
A continuation certificate represents proof that a process is running and can only complete when verifying the certificate.
Each certificate carries a `weight` attribute, which indicates the *logical multiplicity* of the task's execution.
Although a task is physically executed only once, a weight greater than 1 models the task as being *virtually* executed in parallel that many times.
<!-- This is useful for balancing, composing, or distributing continuation chains in advanced scheduling scenarios.
Multiple continuation certificates can be merged into a single one.
A certificate with a multiplicity greater than 1 can be split into multiple certificates. -->

## Operations

### Creating Continuation Monads

- `defer` - creates a continuation monad that defers the subscription until a source is connected (see [example](examples/deferexample.py))
- `from_`: Create a continuation monad from a value:
    ``` python
    c = continuationmonad.from_(5)
    ```
- `get_trampoline` - retrieve trampoline associated with the continuation monad
    ``` python
    c = continuationmonad.get_trampoline()
    ```
- `schedule_on` - schedule elements emitted by the source on a dedicated scheduler
    ``` python
    c = continuationmonad.schedule_on(scheduler)
    ```
- `schedule_trampoline` - schedule item on trampoline
    ``` python
    c = continuationmonad.schedule_trampoline()
    ```
- `tail_rec` - recursively call a function on trampoline


### Transforming operators

- `connect` - connects the continuation monad to deferred one or multiple subscribers (see `defer` operator)
- `flat_map` - apply a function to the item emitted by the source and flattens the result
- `map` - map the item emitted by the source by applying the given function

### Combining operators

- `zip` - create a new continuation monad from two (or more) continuation monads by combining their items in a tuple
    ``` python
    c = continuationmonad.zip((
        continuationmonad.from_(1),
        continuationmonad.from_(2),
    ))
    ```

### Other operators

- `fork` - runs the continuation monad on a specified trampoline
    ``` python
    c = continuationmonad.fork(
        source=c1,
        scheduler=scheduler,
        weight=1,               # specify continuation weight
    )
    ```
- `run` - runs the continuation monad on a new trampoline and returns its result
    ``` python
    result = c.run()            # execute a continuation monad
    ```
