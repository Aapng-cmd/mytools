from pwn import *


target = remote("158.160.96.124", 9001)

target.recvline()
target.recvline()


def g(input_string):

    vowels = 'aeiou'

    vowels_count = 0

    consonants_count = 0


    for char in input_string:

        if char.lower() in vowels:

            vowels_count += 1

        elif char.isalpha():

            consonants_count += 1

    return [str(vowels_count), str(consonants_count)]


while True:
    ask = (target.recvrepeat(0.5)).decode().replace("\r", "").replace("\n", "")
    print(ask)
    ans = ":".join(g(ask))
    target.sendline(ans.encode())

