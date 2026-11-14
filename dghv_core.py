"""Educational secret-key DGHV-style toy implementation.

WARNING: This uses tiny parameters and is NOT cryptographically secure.
It is designed only to demonstrate the arithmetic in the accompanying lesson.
"""
from dataclasses import dataclass
import random

@dataclass
class SecretKey:
    p: int

def centered_remainder(a: int, p: int) -> int:
    """Return the centered representative of a modulo odd p."""
    if p <= 0 or p % 2 == 0:
        raise ValueError("p must be a positive odd integer")
    quotient = (a + p // 2) // p
    return a - quotient * p

def keygen(p: int = 101) -> SecretKey:
    if p <= 2 or p % 2 == 0:
        raise ValueError("Choose an odd p greater than 2")
    return SecretKey(p=p)

def encrypt(bit: int, key: SecretKey, q: int | None = None,
            r: int | None = None) -> int:
    """Encrypt a bit as c = p*q + 2*r + bit."""
    if bit not in (0, 1):
        raise ValueError("This teaching implementation encrypts bits 0 or 1")
    if q is None:
        q = random.randint(100, 1000)
    if r is None:
        r = random.randint(-1, 1)
    return key.p * q + 2 * r + bit

def decrypt(ciphertext: int, key: SecretKey) -> int:
    return centered_remainder(ciphertext, key.p) % 2

def residual(ciphertext: int, key: SecretKey) -> int:
    return centered_remainder(ciphertext, key.p)

def noise_is_within_budget(ciphertext: int, key: SecretKey) -> bool:
    return abs(residual(ciphertext, key)) < key.p / 2

def eval_add(c1: int, c2: int) -> int:
    """Ciphertext addition; after decryption it represents XOR of bits."""
    return c1 + c2

def eval_mul(c1: int, c2: int) -> int:
    """Ciphertext multiplication; after decryption it represents AND of bits."""
    return c1 * c2

def eval_not(c: int, key: SecretKey) -> int:
    """A simple ciphertext expression for NOT: Enc(1) - c."""
    return encrypt(1, key) - c

def eval_or(c1: int, c2: int, key: SecretKey) -> int:
    """OR = a + b + ab over F2; ciphertext evaluation uses + and *."""
    return c1 + c2 + c1 * c2

def evaluate_circuit(a: int, b: int, d: int, key: SecretKey):
    ca = encrypt(a, key, q=7, r=1)
    cb = encrypt(b, key, q=9, r=2)
    cd = encrypt(d, key, q=4, r=1)
    # f(a,b,d) = (a AND b) XOR d
    cab = eval_mul(ca, cb)
    result_cipher = eval_add(cab, cd)
    return {
        "ciphertexts": (ca, cb, cd),
        "result_ciphertext": result_cipher,
        "decrypted_result": decrypt(result_cipher, key),
        "expected_result": (a & b) ^ d,
        "residual": residual(result_cipher, key),
    }
