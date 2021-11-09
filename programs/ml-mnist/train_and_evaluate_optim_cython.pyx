#cython: language_level=3
import timeit
import mnist
import numpy as np

cimport numpy as np
np.import_array()

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

DTYPE2 = np.uint8
ctypedef np.uint8_t DTYPE2_t

DTYPE3 = np.int64
ctypedef np.int64_t DTYPE3_t


def softmax(np.ndarray[DTYPE_t, ndim=1] x):
    cdef np.ndarray[DTYPE_t, ndim=1] e_x = np.exp(np.subtract(x, np.amax(x), dtype=DTYPE), dtype=DTYPE)
    return e_x / np.sum(e_x, dtype=DTYPE)


def forward(np.ndarray[DTYPE_t, ndim=2] x, np.ndarray[DTYPE_t, ndim=2] W0, np.ndarray[DTYPE_t, ndim=2] W1,
            np.ndarray[DTYPE_t, ndim=1] B0, np.ndarray[DTYPE_t, ndim=1] B1):
    cdef np.ndarray[DTYPE_t, ndim=1] y = np.array(x.ravel(), dtype=DTYPE)
    y_arr = [y]
    cdef int l
    cdef np.ndarray[DTYPE_t, ndim=1] v
    # for l in range(2):
    v = W0.T @ y + B0
    y = np.tanh(v, dtype=DTYPE)
    y_arr.append(y)

    v = W1.T @ y + B1
    y = softmax(v)
    y_arr.append(y)
    
    return y_arr


def epoch(np.ndarray[DTYPE_t, ndim=3] train_images, np.ndarray[DTYPE2_t, ndim=1] train_labels,
          np.ndarray[DTYPE_t, ndim=2] W0, np.ndarray[DTYPE_t, ndim=2] W1,
          np.ndarray[DTYPE_t, ndim=1] B0, np.ndarray[DTYPE_t, ndim=1] B1,
          float eta=1e-2):
    cdef np.ndarray[DTYPE3_t, ndim=1] it_indices = np.arange(train_images.shape[0], dtype=DTYPE3)
    np.random.shuffle(it_indices)
    cdef DTYPE3_t i
    cdef np.ndarray[DTYPE_t, ndim=2] x
    cdef DTYPE2_t l
    cdef np.ndarray[DTYPE_t, ndim=1] f0, f1, f2, d, delta_1, delta_2, del_B_1, del_B_2
    cdef np.ndarray[DTYPE_t, ndim=2] del_W_1, del_W_2
    for i in it_indices:
        x = train_images[i]
        l = train_labels[i]
        f0, f1, f2 = forward(x, W0, W1, B0, B1)
        d = np.zeros(10)
        d[l] = 1
        # shape - (N2,)
        delta_2 = (d - f2) * f2 * (1 - f2)
        # shape - (N1,)
        delta_1 = (1 - f1 ** 2) * (W1 @ delta_2)
        del_W_1 = eta * np.outer(f0, delta_1)
        del_B_1 = eta * delta_1
        del_W_2 = eta * np.outer(f1, delta_2)
        del_B_2 = eta * delta_2
        W0 += del_W_1
        B0 += del_B_1
        W1 += del_W_2
        B1 += del_B_2
    return


def train():
    cdef np.ndarray[DTYPE2_t, ndim=3] _train_images = mnist.train_images()
    cdef np.ndarray[DTYPE_t, ndim=2] imean = np.mean(_train_images, axis=0, dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] istd = np.std(_train_images, axis=0, dtype=DTYPE)
    istd[istd == 0] = 1
    cdef np.ndarray[DTYPE_t, ndim=3] train_images = (_train_images - imean) / istd

    cdef np.ndarray[DTYPE2_t, ndim=1] train_labels = mnist.train_labels()

    cdef int N1 = 128
    cdef int N2 = 10
    cdef np.ndarray[DTYPE_t, ndim=2] W0, W1
    cdef np.ndarray[DTYPE_t, ndim=1] B0, B1
    W0, W1 = [np.random.uniform(-1, 1, size=(28 * 28, N1)), np.random.uniform(-1, 1, size=(N1, N2))]
    B0, B1 = [np.random.uniform(-1, 1, size=(N1,)), np.random.uniform(-1, 1, size=(N2,))]

    for _ in range(5):
        epoch(train_images, train_labels, W0, W1, B0, B1, eta=1e-2)
    return
