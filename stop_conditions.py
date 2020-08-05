import time

#stops after t time has passed
def stop_time(t, start=time.time()):
    return lambda path: start + t < time.time()
