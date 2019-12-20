import threading

import time


class InfoThread(threading.Thread):
    def run(self):
        for i in range(2 ** 32):
            for j in range(2 ** 32):
                for k in range(2 ** 32):
                    if ((k+2) ** 4) % ((j+3) ** 4) == 6523523:
                        print(i, j, k)


if __name__ == "__main__":
    threads = 8
    for i in range(threads):
        t = InfoThread()
        t.setDaemon(True)
        t.start()
    while True:
        time.sleep(5)