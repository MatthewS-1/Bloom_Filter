from math import pow, log
import xxhash


class Bloom(object):
    def __init__(self, m=None, n=None, k=None, h=[], P=1 / 1000):
        # m = bit array size; n = number of elements expected; k = number of hash functions;
        # h = array of hash functions; P = probability of false positive
        if n is None:
            raise AttributeError("n can't be none")
        self.n = n
        self.m = m
        if not m:
            self.set_size(P=P)
        self.k = k
        if not k:
            self.set_k()
        self.h = h
        if not h:
            self.set_hash()
        self.bit_arr = [0 for num in range(self.m)]

    def set_hash(self) -> list:
        self.h = [xxhash.xxh32(seed=num) for num in range(self.k)]
        return self.h

    def false_positive(self) -> float:
        return pow(1 - pow(1 - 1 / (self.m), self.k * self.n), self.k)

    def set_size(self, P) -> int:
        self.m = int(-(self.n * log(P)) / pow(log(2), 2))
        return self.m

    def set_k(self) -> int:
        assert self.m and self.n
        self.k = int((self.m / self.n) * log(2))
        return self.k

    def hash_thing(self, thing) -> list:
        hashed = []
        for hash_function in self.h:
            hash_function.update(str.encode(thing))
            byte_hash = hash_function.digest()
            hashed.append(int.from_bytes(byte_hash, byteorder="big"))
            hash_function.reset()
        indices = [num % self.m for num in hashed]
        return indices

    def insert(self, thing) -> None:
        indices = self.hash_thing(thing)
        for i in indices:
            self.bit_arr[i] = 1

    def check(self, thing) -> bool:
        indices = self.hash_thing(thing)
        for i in indices:
            if self.bit_arr[i] == 0:
                return False  # not in bit array
        else:
            return True  # probably in bit array
