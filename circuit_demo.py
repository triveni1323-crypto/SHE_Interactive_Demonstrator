"""Boolean circuit helpers using the educational DGHV toy engine."""
from dghv_core import encrypt, decrypt, eval_add, eval_mul, SecretKey

def half_adder(a: int, b: int, key: SecretKey):
    ca, cb = encrypt(a, key), encrypt(b, key)
    sum_cipher = eval_add(ca, cb)
    carry_cipher = eval_mul(ca, cb)
    return {
        "sum_ciphertext": sum_cipher,
        "carry_ciphertext": carry_cipher,
        "sum": decrypt(sum_cipher, key),
        "carry": decrypt(carry_cipher, key),
        "expected_sum": a ^ b,
        "expected_carry": a & b,
    }

def encrypted_expression(a: int, b: int, d: int, key: SecretKey):
    ca, cb, cd = encrypt(a, key), encrypt(b, key), encrypt(d, key)
    result = eval_add(eval_mul(ca, cb), cd)
    return result, decrypt(result, key), ((a & b) ^ d)
