"""Educational Pedersen-style commitment demonstration.

Uses a tiny toy group for transparency. This is NOT secure.
"""
import secrets

P = 23
Q = 11
G = 2
H = 8  # another element in the order-11 subgroup

def commit(value: int, randomness: int | None = None):
    value %= Q
    if randomness is None:
        randomness = secrets.randbelow(Q)
    c = (pow(G, value, P) * pow(H, randomness, P)) % P
    return c, value, randomness

def verify(commitment: int, value: int, randomness: int) -> bool:
    expected = (pow(G, value % Q, P) * pow(H, randomness % Q, P)) % P
    return commitment == expected

def combine(commitment1: int, commitment2: int) -> int:
    """Homomorphic combination corresponds to adding committed values mod Q."""
    return (commitment1 * commitment2) % P
