# cython: profile=True
import pyximport
pyximport.install()

import skimage.io as io
from skimage import color

import canny_edge_cython


PROFILER = "line_profiler"

# ref: https://github.com/adl1995/edge-detectors
def wrapper():
    img = io.imread("./2011_ford_mustang_gt-2.jpg")
    img = color.rgb2gray(img)
    gauss, magnitude, weak, strong = canny_edge_cython.cannyEdge(
            img, 3, 50, 100)
    io.imsave('out_gauss.jpg', gauss)
    io.imsave('out_magnitude.jpg', magnitude)
    io.imsave('out_weak.jpg', weak)
    io.imsave('out_strong.jpg', strong)

if PROFILER == "cProfile":
    import cProfile
    cProfile.run("canny_edge_cython.main()", "canny_edge_cython_c.stats")
elif PROFILER == "line_profiler":
    # correct usage according to https://stackoverflow.com/a/43377717
    import line_profiler
    prof = line_profiler.LineProfiler()
    prof_wrapper = prof(wrapper)
    prof_wrapper()
    prof.print_stats()
elif PROFILER == "profile":
    import profile
    profile.run("canny_edge_cython.main()", "canny_edge_cython_p.stats")
else:
    import sys
    print("unknown profiler")
    sys.exit(1)
