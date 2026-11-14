import streamlit as st
import pandas as pd
from dghv_core import (
    keygen, encrypt, decrypt, residual, eval_add, eval_mul,
    eval_not, eval_or, evaluate_circuit, noise_is_within_budget
)
from public_key_dghv import keygen as pk_keygen, encrypt as pk_encrypt, evaluate_add, evaluate_multiply, decrypt as pk_decrypt
from pedersen_commitment import commit, verify, combine
from circuit_demo import half_adder
from visualization import noise_growth_figure

st.set_page_config(page_title="SHE Interactive Demonstrator", page_icon="🔐", layout="wide")
st.title("🔐 SHE Interactive Demonstrator")
st.caption("An educational playground for Somewhat Homomorphic Encryption (SHE)")
st.warning("Educational toy implementation only. The small parameters and algorithms here are NOT suitable for protecting real data.")

tabs = st.tabs([
    "Overview", "Secret-key DGHV", "Homomorphic gates", "Noise budget",
    "Public-key DGHV", "Pedersen commitment", "Boolean circuits", "Testing guide"
])

with tabs[0]:
    st.header("What does this application demonstrate?")
    st.markdown("""
    Somewhat Homomorphic Encryption allows selected computations to be performed on ciphertexts.
    The decrypted result corresponds to the same supported computation on the original plaintexts.

    **Main teaching construction:** integer-based DGHV-style toy scheme.

    **Important distinction:** Pedersen commitment is demonstrated separately; it is not a required component of SHE.
    """)
    st.code("Dec(sk, Eval(f, Enc(m1), ..., Enc(mt))) = f(m1, ..., mt)", language="text")
    st.info("Start with the Secret-key DGHV tab, then explore gates, noise, public-key evaluation, commitments and circuits.")

with tabs[1]:
    st.header("Secret-key DGHV: key generation, encryption and decryption")
    p = st.number_input("Secret key p (odd integer)", min_value=3, max_value=10001, value=101, step=2)
    if p % 2 == 0:
        st.error("p must be odd.")
    else:
        sk = keygen(int(p))
        bit = st.selectbox("Plaintext bit", [0, 1], key="sk_bit")
        q = st.number_input("Choose q", value=7, step=1, key="sk_q")
        r = st.number_input("Choose small r", value=1, step=1, key="sk_r")
        if st.button("Encrypt and decrypt", key="sk_run"):
            c = encrypt(int(bit), sk, int(q), int(r))
            st.success("Demonstration completed")
            st.metric("Ciphertext c = p·q + 2r + m", c)
            st.write("Centered remainder [c]p:", residual(c, sk))
            st.metric("Decrypted bit", decrypt(c, sk))
            st.write("Correctness condition |residual| < p/2:", noise_is_within_budget(c, sk))
            st.code(f"{c} = {p} × {q} + 2 × {r} + {bit}")

with tabs[2]:
    st.header("Homomorphic Boolean gates")
    st.write("Choose plaintext bits. The app encrypts them, evaluates a ciphertext expression, then decrypts the result.")
    a = st.selectbox("Input A", [0, 1], key="gate_a")
    b = st.selectbox("Input B", [0, 1], key="gate_b")
    gate = st.selectbox("Gate", ["XOR", "AND", "NOT A", "OR"])
    if st.button("Evaluate gate"):
        sk = keygen(101)
        ca = encrypt(a, sk)
        cb = encrypt(b, sk)
        if gate == "XOR":
            out_c, expected = eval_add(ca, cb), a ^ b
        elif gate == "AND":
            out_c, expected = eval_mul(ca, cb), a & b
        elif gate == "NOT A":
            out_c, expected = eval_not(ca, sk), 1 - a
        else:
            out_c, expected = eval_or(ca, cb, sk), a | b
        actual = decrypt(out_c, sk)
        st.write("Encrypted input A:", ca)
        st.write("Encrypted input B:", cb)
        st.write("Evaluated ciphertext:", out_c)
        st.metric("Decrypted result", actual)
        st.write("Expected Boolean result:", expected)
        st.write("Match:", actual == expected)

with tabs[3]:
    st.header("Noise budget and decryption failure")
    p = st.number_input("Modulus p", min_value=3, max_value=10001, value=101, step=2, key="noise_p")
    initial = st.number_input("Initial residual/noise", min_value=1, max_value=100000, value=3, key="noise_initial")
    levels = st.slider("Repeated squaring levels", min_value=1, max_value=8, value=4)
    if p % 2 == 1:
        fig = noise_growth_figure(int(p), int(initial), int(levels))
        st.pyplot(fig)
        current = int(initial)
        rows = [{"Depth": 0, "Residual magnitude": current, "Within |noise| < p/2": abs(current) < p/2}]
        for depth in range(1, levels + 1):
            current = current ** 2
            rows.append({"Depth": depth, "Residual magnitude": current, "Within |noise| < p/2": abs(current) < p/2})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        st.caption("This plot models illustrative residual growth by repeated squaring; it is not a complete cryptographic noise simulator.")

with tabs[4]:
    st.header("Public-key DGHV teaching demonstration")
    st.write("The evaluator receives the public key and can compute on ciphertexts. The secret key is used only for decryption.")
    if st.button("Generate public/secret key pair"):
        kp = pk_keygen(101)
        st.session_state["kp"] = kp
        st.success("Toy key pair generated.")
        st.write("Public x0:", kp.public_key.x0)
        st.write("Public samples:", list(kp.public_key.samples))
        st.write("Secret p:", kp.secret_key.p)
    if "kp" in st.session_state:
        kp = st.session_state["kp"]
        a = st.selectbox("Public-key plaintext A", [0, 1], key="pk_a")
        b = st.selectbox("Public-key plaintext B", [0, 1], key="pk_b")
        op = st.selectbox("Public-key operation", ["XOR (addition)", "AND (multiplication)"], key="pk_op")
        if st.button("Encrypt, evaluate and decrypt"):
            ca = pk_encrypt(a, kp.public_key)
            cb = pk_encrypt(b, kp.public_key)
            out = evaluate_add(ca, cb) if op.startswith("XOR") else evaluate_multiply(ca, cb)
            result = pk_decrypt(out, kp.secret_key)
            expected = (a ^ b) if op.startswith("XOR") else (a & b)
            st.write("Ciphertext A:", ca)
            st.write("Ciphertext B:", cb)
            st.write("Evaluated ciphertext:", out)
            st.metric("Decrypted result", result)
            st.write("Expected result:", expected)
            st.write("Match:", result == expected)

with tabs[5]:
    st.header("Pedersen commitment (separate cryptographic primitive)")
    st.write("A commitment hides a value while binding the committer to it. It is not SHE encryption.")
    value = st.number_input("Value to commit", value=4, step=1, key="commit_value")
    if st.button("Create commitment"):
        c, v, r = commit(int(value))
        st.session_state["commit_demo"] = (c, v, r)
    if "commit_demo" in st.session_state:
        c, v, r = st.session_state["commit_demo"]
        st.write("Commitment:", c)
        st.write("Opening value:", v)
        st.write("Randomness:", r)
        st.write("Verification:", verify(c, v, r))
        wrong = verify(c, (v + 1) % 11, r)
        st.write("Verification with altered value:", wrong)
        st.caption("Tiny group parameters are intentionally insecure and only suitable for illustrating the equation.")

with tabs[6]:
    st.header("Boolean circuits and half adder")
    a = st.selectbox("Half-adder input A", [0, 1], key="ha_a")
    b = st.selectbox("Half-adder input B", [0, 1], key="ha_b")
    if st.button("Run encrypted half adder"):
        result = half_adder(a, b, keygen(101))
        st.write(result)
        st.success(f"Sum = {result['sum']} (expected {result['expected_sum']}), Carry = {result['carry']} (expected {result['expected_carry']})")
    st.divider()
    st.subheader("Three-input circuit: (A AND B) XOR D")
    a2 = st.selectbox("A", [0, 1], key="circ_a")
    b2 = st.selectbox("B", [0, 1], key="circ_b")
    d2 = st.selectbox("D", [0, 1], key="circ_d")
    if st.button("Evaluate three-input circuit"):
        result = evaluate_circuit(a2, b2, d2, keygen(101))
        st.write("Input ciphertexts:", result["ciphertexts"])
        st.write("Output ciphertext:", result["result_ciphertext"])
        st.metric("Decrypted output", result["decrypted_result"])
        st.write("Expected output:", result["expected_result"])
        st.write("Centered residual:", result["residual"])

with tabs[7]:
    st.header("Automated tests and expected results")
    st.markdown("""
    Open a terminal in the project folder and run:

    ```powershell
    python -m unittest discover -s tests -v
    ```

    The test suite checks centered remainders, encryption/decryption, XOR, AND,
    public-key toy evaluation, Pedersen opening verification and half-adder outputs.
    """)
    st.info("A successful test run ends with OK. Read README.md for the complete setup and run commands.")
