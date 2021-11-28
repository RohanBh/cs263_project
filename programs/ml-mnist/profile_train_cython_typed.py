def profile_all():
    from train_cython_typed import softmax, forward, epoch, train
    import line_profiler

    prof = line_profiler.LineProfiler()
    prof.add_function(softmax)
    prof.add_function(forward)
    prof.add_function(epoch)
    prof_wrapper = prof(train)
    prof_wrapper()
    prof.print_stats()
    return


def time_train():
    from train_cython_typed import train
    import timeit
    import numpy as np

    time_arr = timeit.repeat(train, repeat=5, number=1)
    print('Times:', time_arr)
    print('Median:', np.median(time_arr))
    return



if __name__ == "__main__":
    # time_train()
    profile_all()
