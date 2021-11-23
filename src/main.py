#!/usr/bin/env python3

from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256

## STEP 1: GENERATE A PRIVATE KEY ##
#----------------------------------#
# Ethereum private keys are based on KECCAK-256 hashes (https://keccak.team/keccak.html).
# To generate such a hash we use the `keccak_256` function 
# from the `pysha3` module on a random 32 byte seed:
private_key = keccak_256(token_bytes(32)).digest()

## STEP 2: DERIVE THE PUBLIC KEY FROM THE PRIVATE KEY ##
#------------------------------------------------------#
# To get our public key we need to sign our private key with an
# Elliptic Curve Digital Signature Algorithm (ECDSA).
# Ethereum uses the `secp256k1` curve ECDSA. 
# `coincurve` uses this as a default so we don't need to 
# explicitly specify it when calling the function:
public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]

# The Ethereum Yellow Paper (https://ethereum.github.io/yellowpaper/paper.pdf)
# states that the public key has to be a byte array of size 64. By default 
# `coincurve` uses the compressed format for public keys (`libsecp256k1` 
# was developed for Bitcoin, where compressed keys are commonly used) 
# which is 33 bytes in size. Uncompressed keys are 65 bytes in size.
# Additionally all public keys are prepended with a single byte to indicate
# if they are compressed or uncompressed. This means we first need to get
# the uncompressed 65 byte key (`compressed=False`) and then strip the 
# first byte (`[1:]`) to get our 64 byte Ethereum public key.

## STEP 3: DERIVE THE ETHEREUM ADDRESS FROM THE PUBLIC KEY ##
#-----------------------------------------------------------#
# As specified in the Ethereum Yellow Paper (https://ethereum.github.io/yellowpaper/paper.pdf)
# we take the right most 20 bytes of the 32 byte `KECCAK` hash of the 
# corresponding ECDSA public key.
addr = keccak_256(public_key).digest()[-20:]

print("private_key:", private_key.hex())
print("eth addr: 0x" + addr.hex())
