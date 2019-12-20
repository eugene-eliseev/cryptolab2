from main import get_cryptor, SBOX, to64

if __name__ == "__main__":
    mm = 2 ** 32 - 1
    zero_cryptor = get_cryptor(0)
    sbox_table = []
    for i in range(8):
        sbox_table.append([None for _ in range(16)])
    with open("res.txt", 'r') as res:
        lines = res.readlines()
        for line in lines:
            data = line.strip().split(',')
            if len(data) == 3:
                number, left_part, right_part = data
                number = int(number)
                for i in range(8):
                    for j in range(16):
                        for k in range(16):
                            a = j << 4 * i

                            par1 = 0
                            par2 = 0
                            par_shift = 32 - (4 * i + 11)
                            if par_shift >= 0:
                                par1 = 0x0000000f >> par_shift
                                par2 = k >> par_shift
                            else:
                                par1 = 0x0000000f << -par_shift
                                par2 = k << -par_shift

                            b = (number & (~((15 << (4 * i + 11)) | par1))) | ((k << (4 * i + 11)) | par2)
                            b = (number & (~((15 << (4 * i + 11)) | par1))) | ((k << (4 * i + 11)) | par2)
                            # b = (number & (~(((15 << (4 * i + 11)) & mm) | par1))) | (((k << (4 * i + 11)) & mm) | par2)

                            # b = (number & (~((15 << 4 * i + 11) & (2 ** 32 - 1))) & (2 ** 32 - 1)) | ((k << 4 * i + 11) & (2 ** 32 - 1))

                            # b = (number & ~(15 << 4 * i + 11)) | (k << 4 * i + 11)

                            # if i >= 6:
                            #     b = (number & ~(15 >> -(32 - (4 * i + 11)))) | (k >> -(32 - (4 * i + 11)))

                            text1 = a << 32
                            text2 = (b << 32) | a

                            code1 = zero_cryptor.encrypt(text1 & (2 ** 64 - 1)) & 0xFFFFFFFF
                            code2 = zero_cryptor.encrypt(text2 & (2 ** 64 - 1)) >> 32
                            if code1 == code2:
                                sbox_table[7 - i][j] = k
                            else:
                                pass
                                print(7 - i, j, code1, code2)
                                print(to64(code1))
                                print(to64(code2))
    for i, line in enumerate(sbox_table):
        for j, number in enumerate(line):
            print(number == SBOX[i][j], '', end='')
        print(line)
