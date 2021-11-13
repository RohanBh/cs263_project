#!/usr/bin/env python3
# cython: profile=True
# cython: language_level=3str
import random
import string

PROFILER="line_profiler"

def write_random_bytes(int n):
    out = random.choices(string.ascii_letters, [1] * len(string.ascii_letters), k=n)
    out_s = "".join(out)
    with open("test.file", "w") as f:
        f.write(out_s)

def read_bytes(int n):
    with open("test.file", "r") as f:
        in_bytes = f.read(n)
    return in_bytes

def run():
    n = 2000000
    write_random_bytes(n)
    read_bytes(n)
