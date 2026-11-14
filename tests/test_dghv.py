import unittest
from dghv_core import keygen, encrypt, decrypt, centered_remainder, eval_add, eval_mul

class TestDGHV(unittest.TestCase):
    def setUp(self):
        self.key = keygen(101)

    def test_centered_remainder(self):
        self.assertEqual(centered_remainder(710, 101), 3)
        self.assertEqual(centered_remainder(648940, 101), 15)
        self.assertEqual(centered_remainder(-81, 101), 20)

    def test_encrypt_decrypt(self):
        for bit in (0, 1):
            c = encrypt(bit, self.key, q=7, r=1)
            self.assertEqual(decrypt(c, self.key), bit)

    def test_xor(self):
        for a in (0, 1):
            for b in (0, 1):
                ca, cb = encrypt(a, self.key), encrypt(b, self.key)
                self.assertEqual(decrypt(eval_add(ca, cb), self.key), a ^ b)

    def test_and(self):
        for a in (0, 1):
            for b in (0, 1):
                ca, cb = encrypt(a, self.key), encrypt(b, self.key)
                self.assertEqual(decrypt(eval_mul(ca, cb), self.key), a & b)

if __name__ == "__main__":
    unittest.main()
