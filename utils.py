import random


def gen_password(__password_len__=8):
    table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ans = ''
    for i in range(__password_len__):
        ans += table[random.randint(0, len(table) - 1)]
    return ans
