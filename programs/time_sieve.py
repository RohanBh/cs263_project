import pyximport
pyximport.install()

from sieve_of_eratosthenes_cython import main
import timeit



if __name__ == "__main__":
    print(timeit.timeit(main, number=100))
