import unittest
from public_key_dghv import keygen as pk_keygen, encrypt as pk_encrypt, evaluate_add, evaluate_multiply, decrypt as pk_decrypt
from pedersen_commitment import commit, verify
from circuit_demo import half_adder
from dghv_core import keygen

class TestOtherModules(unittest.TestCase):
    def test_public_key_xor_and(self):
        kp = pk_keygen(101)
        for a in (0, 1):
            for b in (0, 1):
                ca, cb = pk_encrypt(a, kp.public_key), pk_encrypt(b, kp.public_key)
                self.assertEqual(pk_decrypt(evaluate_add(ca, cb), kp.secret_key), a ^ b)
                self.assertEqual(pk_decrypt(evaluate_multiply(ca, cb), kp.secret_key), a & b)

    def test_commitment(self):
        c, v, r = commit(4, randomness=3)
        self.assertTrue(verify(c, v, r))
        self.assertFalse(verify(c, v + 1, r))

    def test_half_adder(self):
        for a in (0, 1):
            for b in (0, 1):
                result = half_adder(a, b, keygen(101))
                self.assertEqual(result["sum"], a ^ b)
                self.assertEqual(result["carry"], a & b)

if __name__ == "__main__":
    unittest.main()
