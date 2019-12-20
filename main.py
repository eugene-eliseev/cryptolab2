import multiprocessing
import time
from gost import GostCrypt

# import numpy.random
# import itertools

# SBOX = [numpy.random.permutation(l) for l in itertools.repeat(range(16), 8)]
SBOX = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)


def get_cryptor(key):
    return GostCrypt(key, SBOX)


def to64(num):
    r = str(bin(num))[2:]
    while len(r) < 64:
        r = '0' + r
    return r


def hack(data):
    num, start, end, print_freq = data
    zero_cryptor = get_cryptor(0)
    zero_enc = zero_cryptor.encrypt(0)
    # part2 = to64(zero_enc)[32:]
    part2 = zero_enc & 0xFFFFFFFF  # оптимизация
    time_start = time.time()
    print("# {} # Start work {} - {}".format(num, start, end))
    for i in range(start, end):
        if i % print_freq == 0:
            print("# {} # Done {} in {} s".format(num, i, int(time.time() - time_start)))
        # part1 = to64(zero_cryptor.encrypt(i << 32))[:32]
        # if part1 == part2:
        part1 = zero_cryptor.encrypt(i << 32) >> 32  # оптимизация
        if part1 == part2:
            print("# {} #".format(num), i, part1, part2)
            with open("res.txt", "a+") as f:
                f.write("{},{},{}".format(i, part1, part2))
                f.flush()


if __name__ == "__main__":
    cluster_id = 0
    cluster_num = 2
    threads = 16
    freq = 1000000
    end = 2 ** 32
    one_t_step = end // threads
    data = []
    p = multiprocessing.Pool(processes=8)
    for i in range(threads):
        if i % cluster_num == cluster_id:
            data.append((i, i * one_t_step, (i + 1) * one_t_step, freq))
    p.map(hack, data)
