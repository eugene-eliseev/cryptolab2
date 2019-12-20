import multiprocessing
import time

from gost import GostCrypt

SBOX = (
    (0, 2, 1, 3, 5, 4, 6, 8, 9, 7, 14, 13, 10, 11, 15, 12),
    (1, 0, 2, 12, 14, 15, 11, 10, 13, 3, 7, 4, 5, 6, 8, 9),
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
    (15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
    (0, 2, 1, 3, 5, 4, 6, 8, 9, 7, 14, 13, 10, 11, 15, 12),
    (1, 0, 2, 12, 14, 15, 11, 10, 13, 3, 7, 4, 5, 6, 8, 9),
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
    (15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
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
    part2 = zero_enc & 0xFFFFFFFF  # оптимизация
    time_start = time.time()
    print("# {} # Start work {} - {}".format(num, start, end))
    # for i in range(start, end): # можно реально перебирать, но число мы уже знаем, а питон оч медленный =(
    for i in [2013820936]:
        i = i & (2 ** 32 - 1)
        if i % print_freq == 0:
            print("# {} # Done {} in {} s".format(num, i, int(time.time() - time_start)))
        part1 = zero_cryptor.encrypt(i << 32) >> 32  # оптимизация
        if part1 == part2:
            print("# {} #".format(num), i, part1, part2)
            with open("res.txt", "a+") as f:
                f.write("{},{},{}\n".format(i, part1, part2))
                f.flush()


if __name__ == "__main__":
    # распределённый взлом =)
    cluster_id = 0
    cluster_num = 1
    threads = 1
    freq = 1000000
    end = 2 ** 32
    one_t_step = end // threads
    data = []
    p = multiprocessing.Pool(processes=8)
    for i in range(threads):
        if i % cluster_num == cluster_id:
            data.append((i, i * one_t_step, (i + 1) * one_t_step, freq))
    p.map(hack, data)
