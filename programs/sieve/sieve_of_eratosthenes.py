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

    # for i in range(2, n+1):
    #     if arr[i]:
    #         print(i)
    # print('Total primes:')
    # print(len([1 for x in arr if x]) - 2)
    return


def main():
    sieve(2000000)
    return
