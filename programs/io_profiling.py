#!/usr/bin/env python3
import random
import string

PROFILER="line_profiler"

def write_random_bytes(n):
    out = random.choices(string.ascii_letters, [1] * len(string.ascii_letters), k=n)
    out = "".join(out)
    with open("test.file", "w") as f:
        f.write(out)

def read_bytes(n):
    with open("test.file", "r") as f:
        in_bytes = f.read(n)
    return in_bytes

def run():
    n = 20000
    write_random_bytes(n)
    read_bytes(n)

if PROFILER == "cProfile":
    import cProfile
    cProfile.run("run()", "io_profiling_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_wrapper = prof(run)
    prof_wrapper()
    prof.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("run()", "io_profiling_p.stats")
else:
    import sys
    print("unknown profiler")
    sys.exit(1)

