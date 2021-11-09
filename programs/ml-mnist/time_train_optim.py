from train_and_evaluate_optim_cython import train
import timeit
import numpy as np


def time_train():
    time_arr = timeit.repeat(train, repeat=5, number=1)
    print('Times:', time_arr)
    print('Median:', np.median(time_arr))
    return



if __name__ == "__main__":
    time_train()
