import continuationmonad


s1 = continuationmonad.init_event_loop_scheduler()
s2 = continuationmonad.init_event_loop_scheduler()

c1 = continuationmonad.schedule_with_delay(s1, 0.1).map(lambda _: 1)
c2 = continuationmonad.schedule_on(s2).map(lambda _: 2)

result = continuationmonad.zip((c1, c2)).run()

print(result)
