import continuationmonad


def count_down(count: int):
    print(f"{count=}")

    if count == 0:
        return continuationmonad.from_(count)

    else:
        # schedule recursive call on the trampoline
        return continuationmonad.tail_rec(lambda: count_down(count - 1))

result = continuationmonad.run(
    count_down(5)
)

print(f'{result=}')
