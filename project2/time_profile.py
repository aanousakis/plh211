import time
import timeit

import resource
import os



start_time = timeit.default_timer()
time.sleep(1)
#print(timeit.default_timer() - start_time)


a = [1] * (10 ** 6)
b = [2] * (2 * 10 ** 8)
del b

kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss # peak memory usage (bytes on OS X, kilobytes on Linux)
megabytes = kilobytes / 1024

print("Max memory usage : " + str(megabytes) + "MB")

#print(gigabytes)
