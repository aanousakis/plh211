import time
import timeit

import resource
import os

#@profile
def test():
    start_time = timeit.default_timer()
    time.sleep(1)
    #print(timeit.default_timer() - start_time)


    kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss # peak memory usage (bytes on OS X, kilobytes on Linux)
    gigabytes = kilobytes / 1024

    #print(gigabytes)

#@profile
def my_func():

    test()

    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 9)
    del b
    return a

if __name__ == '__main__':
    my_func()
