import continuationmonad


def count_down(count: int):
    print(f'{count=}')

    if count == 0:
        return continuationmonad.from_(count)
    
    else:
        return continuationmonad.schedule_trampoline().flat_map(
            lambda _: count_down(count - 1)
        )

# Runs the continuation and returns 0
result = continuationmonad.run(
    count_down(5)
)