#cython: language_level=3
import timeit
import mnist
import numpy as np


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def forward(x, W, B):
    y = np.array(x.ravel())
    y_arr = [y]
    for l in range(2):
        v = W[l].T @ y + B[l]
        if l == 0:
            y = np.tanh(v)
        else:
            y = softmax(v)
        y_arr.append(y)
    return y_arr


def epoch(train_images, train_labels, W, B, eta=1e-2):
    it_indices = np.arange(train_images.shape[0])
    np.random.shuffle(it_indices)
    for i in it_indices:
        x = train_images[i]
        l = train_labels[i]
        f = forward(x, W, B)
        d = np.zeros(10)
        d[l] = 1
        # shape - (N2,)
        delta_2 = (d - f[2]) * f[2] * (1 - f[2])
        # shape - (N1,)
        delta_1 = (1 - f[1] ** 2) * (W[1] @ delta_2)
        del_W_1 = eta * np.outer(f[0], delta_1)
        del_B_1 = eta * delta_1
        del_W_2 = eta * np.outer(f[1], delta_2)
        del_B_2 = eta * delta_2
        W[0] += del_W_1
        B[0] += del_B_1
        W[1] += del_W_2
        B[1] += del_B_2
    return


def train():
    train_images = mnist.train_images()
    imean = np.mean(train_images, axis=0)
    istd = np.std(train_images, axis=0)
    istd[istd == 0] = 1
    train_images = (train_images - imean) / istd

    train_labels = mnist.train_labels()

    N1 = 128
    N2 = 10
    W = [np.random.uniform(-1, 1, size=(28 * 28, N1)), np.random.uniform(-1, 1, size=(N1, N2))]
    B = [np.random.uniform(-1, 1, size=(N1,)), np.random.uniform(-1, 1, size=(N2,))]

    for _ in range(5):
        epoch(train_images, train_labels, W, B, eta=1e-2)
    return
