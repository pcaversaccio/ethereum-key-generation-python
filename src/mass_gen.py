#!/usr/bin/env python3

from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256

def generate_address():
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]
    return private_key.hex(), addr.hex()

if __name__ == '__main__':
    import timeit
    print(timeit.timeit(
        stmt="generate_address()",
        setup="from __main__ import generate_address",
        number=10**6))
