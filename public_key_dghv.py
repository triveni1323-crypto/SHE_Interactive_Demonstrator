"""Small educational public-key DGHV-style demonstration.

This is a toy illustration, not a secure parameter generation procedure.
"""
from dataclasses import dataclass
import random
from dghv_core import centered_remainder, decrypt as secret_decrypt, SecretKey

@dataclass
class PublicKey:
    x0: int
    samples: tuple[int, ...]

@dataclass
class KeyPair:
    secret_key: SecretKey
    public_key: PublicKey

def keygen(p: int = 101, sample_count: int = 4) -> KeyPair:
    if p <= 2 or p % 2 == 0:
        raise ValueError("p must be an odd integer greater than 2")
    # x0 is odd, while its centered residue modulo p is even.
    while True:
        q0 = random.choice(range(101, 501, 2))
        e0 = random.choice([-4, -2, 2, 4])
        x0 = p * q0 + e0
        if x0 % 2 == 1 and centered_remainder(x0, p) % 2 == 0:
            break
    samples = []
    for _ in range(sample_count):
        q = random.randint(100, 500)
        e = random.randint(-1, 1)
        samples.append(p * q + e)
    return KeyPair(SecretKey(p), PublicKey(x0, tuple(samples)))

def encrypt(bit: int, public_key: PublicKey, r: int | None = None,
            subset: list[int] | None = None) -> int:
    if bit not in (0, 1):
        raise ValueError("Only bits 0 and 1 are supported")
    if r is None:
        r = 0
    if subset is None:
        subset = random.sample(range(len(public_key.samples)),
                               k=random.randint(0, min(1, len(public_key.samples))))
    value = bit + 2 * r + 2 * sum(public_key.samples[i] for i in subset)
    return centered_remainder(value, public_key.x0)

def evaluate_add(c1: int, c2: int) -> int:
    return c1 + c2

def evaluate_multiply(c1: int, c2: int) -> int:
    return c1 * c2

def decrypt(ciphertext: int, secret_key: SecretKey) -> int:
    return secret_decrypt(ciphertext, secret_key)
