import continuationmonad

c = continuationmonad.zip((
    continuationmonad.from_(1),
    continuationmonad.from_(2),
))

result = continuationmonad.run(c)
print(result)
