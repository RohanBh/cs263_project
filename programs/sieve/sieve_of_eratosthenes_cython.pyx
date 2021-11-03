#cython: language_level=3

def sieve(n=100):
    arr = [True for _ in range(n+1)]
    # i -- smallest prime so far
    i = 2
    while i <= n:
        for j in range(2*i, n+1, i):
            arr[j] = False
        found = False
        for j in range(i+1, n+1, 1):
            if arr[j]:
                i = j
                found = True
                break
        if not found:
            break
    return


def main():
    sieve(20000000)
    return
