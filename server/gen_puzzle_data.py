import random
import datetime


ALPHABET = 'abcdefghijklmopqrstuvwxyz'


def n_bits(num, n):
    '''
    Returns the bottom `n` bits from `num`
    '''
    return num & ((1<<n)-1)


def hash(w, seed):
    '''
    Returns the hash of the string `w` with the integer seed `seed`
    '''
    h = seed
    for c in w:
        h = (((h<<5)-h) + ord(c)) ^ seed
    return h


def gen_seeds():
    '''
    Returns a two  seeds: first is 24 bits long, second is 8 bits long
    '''
    k1 = random.randint(0, 1<<24)
    k2 = random.randint(0, 1<<8)
    return (k1, k2)


def word_compare(w, ans):
    '''
    Compares the word `w` to the answer `ans`.
    Example: if w=chogs and ans=ghost then the comparison is 20011
    because c is not in ghost (2), h is in the right spot (0), and
    s is in the answer but in the wrong place (1)
    Returns: the decimal version of the reverse ternary comparison,
    so for 20011 it returns 110 decimal
    Assumes len(w) == len(ans)
    '''
    o = 0
    for i in range(0, len(w)):
        if w[i] == ans[i]: continue
        elif w[i] in ans: o += 3**i
        else: o += 2*(3**i)
    return o


def gen_table(answer, words, s1, s2):
    '''
    Given the string answer, and the list of dictionary words, the
    24-bit seed `s1` for the keyspace, and the 8-bit seed for the
    valuespace, this function returns a python dictionary whose keys
    are the 24-bit hashes of the dictionary words, and values are
    the 8b-bit comparisons to the answer salted with the hash of the
    word.
    '''
    return { n_bits(hash(w,s1), 24):
             n_bits(word_compare(w,answer) ^ hash(w,s2), 8)
             for w in words }


def dump_table(s1, s2, table, filename):
    '''
    Dumps a table whose keys are 24-bits long and values are 8-bits
    long into the file whose name is the string `filename`.
    Since 24+8=32, every entry takes one integer.
    To ease the searching on the user's end the keys will be dumped
    in sorted order, enabling binary search.
    Since the key occupies the top 24-bits of the integer, effectively
    after smashing the keys and values together, the whole list is
    sorted, then dumped to a file.
    The two seeds are also dumped to the file at the very top
    Nothing is returned
    '''
    data = [(k<<8)+v for (k,v) in table.items()]
    data.sort()
    bytes = bytearray([0]*(4+4*len(data)))
    bytes[0] = (s1 >> 16) & 0xff
    bytes[1] = (s1 >> 8)  & 0xff
    bytes[2] = s1         & 0xff
    bytes[3] = s2
    for i in range(len(data)):
        datum = data[i]
        bytes[4*i+4] = (datum >> 24) & 0xff
        bytes[4*i+5] = (datum >> 16) & 0xff
        bytes[4*i+6] = (datum >>  8) & 0xff
        bytes[4*i+7] = datum         & 0xff
    f = open(filename, 'wb')
    f.write(bytes)
    f.close()


now = datetime.datetime.now()
print("-"*20)
print(now.strftime("%Y-%m-%d %H:%M:%S"))
print("-"*20)

tries = 0
words = list(filter(lambda x: len(x)==5, map(lambda x: x[:-1],
                    open("dict.txt").readlines())))
answer = random.choice(words)
print("Dictionary contains %d words" % len(words))

while True:
    tries += 1
    s1, s2 = gen_seeds()
    print("Using seeds %d and %d," % (s1, s2), end=" ")

    table = gen_table(answer, words, s1, s2)
    collisions = len(words) - len(table)
    print("table has %d keys, there are %d collisions" %
            (len(table), collisions))

    if collisions > 0: continue

    print("No collision found after", tries, "trie(s)")
    dump_table(s1, s2, table, "data.bin")
    print("Wrote the seeds and the table to data.bin")

    break

print("Answer of the day is %s" % answer)
