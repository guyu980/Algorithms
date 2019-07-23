from random import choice
import matplotlib.pyplot as plt


class HashTable:
    def __init__(self, h, n):
        self.h = h
        self.buckets = [[] for i in range(n)]

    def insert(self, x):
        self.buckets[self.h(x)].append(x)

    def delete(self, x):
        bucket = self.buckets[self.h(x)]

        for i in range(len(bucket)):
            if bucket[i] == x:
                return bucket.pop(i)

        return None

    def find(self, x):
        bucket = self.buckets[self.h(x)]

        for i in range(len(bucket)):
            if bucket[i] == x:
                return bucket[i]

        return None

    def __repr__(self):
        table = ''

        for i in range(len(self.buckets)):
            table += '     Class %2d: ' % i + str(self.buckets[i]) + '\n'

        return table


def least_sig_dig(x, n=10):
    return x % n


def most_sig_dig(x, n=10):
    last = 0

    while x > 0:
        last = x % n
        x = x // n

    return last


def generate_universal_hash_func(a, b, p, n=10):
    def f(x):
        r = (a * x + b) % p
        return r % n
    return f


def bad_hash_family():
    return choice([least_sig_dig, most_sig_dig])


def good_hash_family():
    a = choice(range(1, p))
    b = choice(range(p))
    return generate_universal_hash_func(a, b, p)


def get_collision_prob(hash_family, M, trials=100):
    data = []

    for x in range(M):
        for y in range(x+1, M):
            count = 0

            for t in range(trials):
                h = hash_family()

                if h(x) == h(y):
                    count += 1

            data.append(count / trials)

    return data


if __name__ == '__main__':
    M = 100
    n = 10
    p = 101

    data_bad = get_collision_prob(bad_hash_family, M)
    data_good = get_collision_prob(good_hash_family, M)

    counts, bins, patchs = plt.hist([data_bad, data_good], color=['orange', 'blue'],
                                    label=['not good hash family', 'universal hash family'], bins=10)
    plt.legend()
    plt.xticks(bins)
    plt.xlabel('Probability of collision')
    plt.ylabel('Number of pairs of elements')
    plt.show()
