# SHE Interactive Demonstrator

An educational Python + Streamlit project demonstrating a toy integer-based DGHV-style SHE construction, Boolean gates, noise growth, a public-key DGHV teaching example, Pedersen commitments, and circuits.

> **Security warning:** All parameters are tiny and deliberately insecure. This project is for classroom learning only. Do not use it to protect real data.

## 1. Requirements

- Windows 10/11
- Python 3.10 or newer
- VS Code
- Internet access for installing packages

## 2. Open the project

Extract the ZIP. In VS Code choose **File → Open Folder** and select `SHE_Interactive_Demonstrator`.

Open **Terminal → New Terminal**.

## 3. Create and activate a virtual environment (PowerShell)

```powershell
python --version
python -m pip --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

The terminal should show `(.venv)` at the beginning of the prompt.

## 4. Install packages

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Expected: pip reports that Streamlit, Pandas and Matplotlib are installed.

## 5. Run the application

```powershell
python -m streamlit run app.py
```

Expected: Streamlit prints a local URL, usually `http://localhost:8501`, and opens the application in your browser. If it does not open automatically, copy the URL into your browser.

Stop the app with `Ctrl+C` in the terminal.

## 6. Run automated tests

```powershell
python -m unittest discover -s tests -v
```

Expected ending:

```text
Ran 7 tests in ...
OK
```

## 7. Files

- `dghv_core.py`: secret-key toy DGHV operations and noise helpers.
- `public_key_dghv.py`: public-key toy DGHV illustration.
- `pedersen_commitment.py`: separate Pedersen commitment demonstration.
- `circuit_demo.py`: half-adder and Boolean circuit helpers.
- `visualization.py`: noise-growth plot.
- `app.py`: Streamlit interface.
- `tests/`: automated tests.

## 8. Mathematical notes

Secret-key teaching encryption:

`c = p*q + 2*r + m`

Decryption:

`m = [c]_p mod 2`

where `[c]_p` is the centered remainder. The simple correctness condition is that the centered residual remains smaller in magnitude than `p/2`.

For bits, homomorphic addition corresponds to XOR and multiplication corresponds to AND, provided the noise remains within the correctness range.

The public-key and commitment tabs are simplified classroom demonstrations, not implementations suitable for cryptographic deployment.
