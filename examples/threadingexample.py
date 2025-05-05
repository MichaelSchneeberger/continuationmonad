import continuationmonad


s1 = continuationmonad.init_event_loop_scheduler()
s2 = continuationmonad.init_event_loop_scheduler()

c1 = continuationmonad.schedule_relative(s1, 12).map(lambda _: 1)
c2 = continuationmonad.schedule_on(s2).map(lambda _: 2)

result = continuationmonad.run(
    continuationmonad.zip((c1, c2))
)

print(result)
