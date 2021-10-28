# cython: language_level=3
# cython: profile=True
import line_profiler
import pyximport
pyximport.install()

from sieve_of_eratosthenes import *

PROFILER = "line_profiler"

def call_sieve():
    n = 200000
    sieve(n)
    return


if __name__ == "__main__":
    # correct usage according to https://stackoverflow.com/a/43377717
    prof = line_profiler.LineProfiler()
    prof_sieve = prof(call_sieve)
    prof_sieve()
    prof.print_stats()
