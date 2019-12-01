import time
import timeit

import resource
import os
filename = 'test'

def foo1():
     with open(filename, "r") as filehandle:
        iterator = iter(filehandle)
        done_looping = False

        while not done_looping:
            try:
                line = next(iterator)
            except StopIteration:
                done_looping = True
            else:
                #print(line)
                pass


            


def foo2():
    with open(filename, "r") as filehandle:
        for line in filehandle:
            #print(line)
            pass


if __name__ == '__main__':
    

    start_time = timeit.default_timer()
    foo2()
    print("foo2 Executed in " ,timeit.default_timer() - start_time, "seconds")

    start_time = timeit.default_timer()
    foo1()
    print("foo2 Executed in " ,timeit.default_timer() - start_time, "seconds")

    kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss # peak memory usage (bytes on OS X, kilobytes on Linux)
    megabytes = kilobytes / 1024

    print("Max memory usage : " + str(megabytes) + "MB")