#!/usr/bin/env python3
"""Print the content of a statistic file produced by cProfile. """

import sys
import pstats

def usage():
    print(f"usage: {sys.argv[0]} <path/to/stat-file> [filter]\n")

if len(sys.argv) < 2:
    usage()
    sys.exit(1)

stat = pstats.Stats(sys.argv[1])
if len(sys.argv) == 3:
    print("test")
    stat.print_stats(sys.argv[2])
else:
    stat.print_stats()
