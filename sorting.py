from random import choice


# O(n^2)
def insertion_sort(A):
    for i in range(1, len(A)):
        current = A[i]
        j = i - 1

        while current < A[j] and j >= 0:
            A[j + 1] = A[j]
            j -= 1

        A[j + 1] = current

    return A


# O(nlog(n))
def merge_sort(A):
    n = len(A)

    if n == 1:
        return A

    L = merge_sort(A[:n // 2])
    R = merge_sort(A[n // 2:])

    return merge(L, R)


def merge(L, R):
    i, j = 0, 0
    M = []

    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            M.append(L[i])
            i += 1
        else:
            M.append(R[j])
            j += 1

    while i < len(L):
        M.append(L[i])
        i += 1

    while j < len(R):
        M.append(R[j])
        j += 1

    return M


# O(nlog(n)) ~ O(n^2)
def get_pivot(A):
    return choice(range(len(A)))


def quick_sort(A):
    if len(A) <= 1:
        return A

    p = get_pivot(A)
    L, R, P = [], [], [A[p]]

    for i in range(len(A)):
        if i == p:
            continue

        if A[i] < A[p]:
            L.append(A[i])
        elif A[i] > A[p]:
            R.append(A[i])
        else:
            P.append(A[i])

    return quick_sort(L) + P + quick_sort(R)


def get_digits(x, base):
    digits = []
    while x > 0:
        digits.append(x % base)
        x = x // base
    return digits


class MyInt:
    def __init__(self, x, base=10, key_digit=0):
        self.digits = get_digits(x, base)
        self.key_digit = key_digit
        self.value = x

    def key(self):
        if len(self.digits) > self.key_digit:
            return self.digits[self.key_digit]
        return 0

    def update_key_digit(self, p):
        self.key_digit = p

    def get_value(self):
        return self.value


class MyQueue:
    def __init__(self):
        self.lst = []

    def push(self, x):
        self.lst.append(x)

    def pop(self):
        return self.lst.pop(0)

    def get_list(self):
        return self.lst


def bucket_sort(A, bucket_max=10):
    T = [MyQueue() for i in range(bucket_max)]

    for x in A:
        T[x.key()].push(x)

    ret = []

    for i in range(bucket_max):
        ret += T[i].get_list()

    return ret


# O(n) for sorting n integers of size at most n^C
def radix_sort(A, n_digits, base=10):
    B = [MyInt(x, base=base) for x in A]

    for j in range(n_digits):
        for x in B:
            x.update_key_digit(j)

        B = bucket_sort(B, bucket_max=base)

    return B


def partition(A, p):
    L, R = [], []

    for i in range(len(A)):
        if i == p:
            continue

        if A[i] < A[p]:
            L.append(A[i])
        else:
            R.append(A[i])

    return L, R, A[p]


def select(A, k):
    p = get_pivot(A)
    L, R, pivot = partition(A, p)

    if len(L) == k-1:
        return pivot
    elif len(L) > k-1:
        return select(L, k)
    else:
        return select(R, k-len(L)-1)


if __name__ == '__main__':
    print('=============================================================')
    A = [6, 2, 10, 1, 5, 8, 3, 9, 7, 4]
    B = insertion_sort(A[:])
    C = merge_sort(A[:])
    print('     - List:\n          ', A)
    print('     - Insertion Sort:\n          ', B)
    print('     - Merge Sort:\n          ', C)
    print('=============================================================')
    D = [6, 3, 2, 7, 10, 4, 1, 9, 5, 6, 8, 2, 3, 9, 7, 4, 8, 1, 10, 5]
    E = quick_sort(D[:])
    print('     - List:\n          ', D)
    print('     - Quick Sort:\n          ', E)
    print('=============================================================')
    F = [MyInt(x) for x in [5, 4, 3, 2, 1, 2, 3, 4, 5]]
    print('     - List:\n          ', [f.get_value() for f in F])
    print('     - Bucket Sort:\n          ', [a.key() for a in bucket_sort(F)])

    G = [523, 123, 4, 33, 12]
    H = radix_sort(G, 3, 10)
    print('     - List:\n          ', G)
    print('     - Radix Sort:\n          ', [h.get_value() for h in H])
    print('=============================================================')
    print('     - List:\n          ', A)
    print('     - The %d-th smallest number is: %d' % (4, select(A, 4)))
    print('=============================================================')
