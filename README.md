# Generating Ethereum Addresses in Python
Due to its slow interpreter, Python is usually not a good choice when it comes to writing performant applications. The exception being Python modules which use an interface that calls C/C++ code. These modules are usually very fast, popular examples are [TensorFlow](https://www.tensorflow.org), [NumPy](https://numpy.org), or [SciPy](https://scipy.org). The steps for interfacing Python with C using [`ctypes`](https://docs.python.org/3.9/library/ctypes.html) are usually:
1. Write C code functions.
2. Compile the C code as a shared library.
3. Write some Python code lines to _extract_ the C functions from the shared library.
4. Run.

Now, to generate Ethereum addresses we can use the following two Python modules which are both `C` based and have a good performance:
- [coincurve](https://github.com/ofek/coincurve): Cross-platform Python CFFI bindings for `libsecp256k1`.
- [pysha3](https://github.com/tiran/pysha3): `SHA-3` wrapper for Python (with support for keccak).

Generating Ethereum addresses is a **3-step** process:
1. Generate a private key.
2. Derive the public key from the private key.
3. Derive the Ethereum address from the public key.
> Note that public keys and Ethereum addresses are not the same. Addresses are hashes of public keys. It's not possible to send funds to a public key.

## Full Example Code With Explanation
```python
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

print('private_key:', private_key.hex())
print('eth addr: 0x' + addr.hex())
```
You can find the original source file [here](https://github.com/pcaversaccio/ethereum-key-generation-python/blob/main/src/main.py).
> In addition, there is another file called [`mass_keygen.py`](https://github.com/pcaversaccio/ethereum-key-generation-python/blob/main/src/mass_keygen.py) that can be used to generate any number of Ethereum addresses. Currently, the threshold is set to 1'000'000.

# Reference
[1] https://www.arthurkoziel.com/generating-ethereum-addresses-in-python
