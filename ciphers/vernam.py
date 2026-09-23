import secrets
import string
from typing import List, Dict, Tuple, Any

KEY_ALPHABET = string.ascii_letters + string.digits


def generate_vernam_key(length: int) -> str:
    """Generates a random printable one-time key using a CSPRNG."""
    if length <= 0:
        raise ValueError("Panjang kunci harus lebih dari 0.")
    return "".join(secrets.choice(KEY_ALPHABET) for _ in range(length))


def _printable(b: int) -> str:
    return chr(b) if 32 <= b < 127 else "."


def vernam_xor_bytes(data: bytes, key: bytes) -> Tuple[bytes, List[Dict[str, Any]]]:
    """
    Core Vernam operation: C_i = P_i XOR K_i (bitwise, per byte).
    XOR is its own inverse, so the same function encrypts and decrypts.
    The key must be exactly as long as the data (one-time pad rule).
    """
    if len(key) != len(data):
        raise ValueError(
            f"Panjang kunci Vernam ({len(key)} byte) harus sama persis dengan panjang data ({len(data)} byte)."
        )
    out = bytearray()
    steps = []
    for i, (d, k) in enumerate(zip(data, key)):
        x = d ^ k
        out.append(x)
        steps.append({
            "index": i + 1,
            "in_char": _printable(d),
            "in_dec": d,
            "in_bin": f"{d:08b}",
            "key_char": _printable(k),
            "key_bin": f"{k:08b}",
            "xor_bin": f"{x:08b}",
            "out_dec": x,
            "out_hex": f"{x:02X}",
            "out_char": _printable(x),
        })
    return bytes(out), steps


def encrypt_vernam(plaintext: str, key: str) -> Tuple[str, List[Dict[str, Any]]]:
    """Encrypts text with a Vernam cipher. Returns (ciphertext_hex, steps)."""
    cipher, steps = vernam_xor_bytes(plaintext.encode("utf-8"), key.encode("utf-8"))
    return cipher.hex().upper(), steps


def decrypt_vernam(cipher_hex: str, key: str) -> Tuple[str, List[Dict[str, Any]]]:
    """Decrypts a hex ciphertext produced by encrypt_vernam."""
    try:
        cipher = bytes.fromhex("".join(cipher_hex.split()))
    except ValueError:
        raise ValueError("Ciphertext Vernam harus berupa string heksadesimal yang valid.")
    plain, steps = vernam_xor_bytes(cipher, key.encode("utf-8"))
    try:
        return plain.decode("utf-8"), steps
    except UnicodeDecodeError:
        raise ValueError("Hasil dekripsi bukan teks UTF-8 yang valid (kunci kemungkinan salah).")
