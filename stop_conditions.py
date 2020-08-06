import time

#stops after t time has passed
def stop_time(t, start):
    return lambda path: start + t < time.time()
