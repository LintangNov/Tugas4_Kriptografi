from typing import Dict, Any, Tuple
from ciphers.vigenere import encrypt_vigenere, decrypt_vigenere
from ciphers.playfair import encrypt_playfair, decrypt_playfair
from ciphers.lfsr import lfsr_crypt_bytes
from ciphers.vernam import vernam_xor_bytes, generate_vernam_key


def _hex(b: bytes) -> str:
    return b.hex().upper()


def super_encrypt(
    plaintext: str,
    key_vig: str,
    key_playfair: str,
    lfsr_seed: str,
    lfsr_n: int,
    vernam_key: str = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Executes 4-layer sequential Super Encryption:
    Plaintext -> [1. Playfair]     -> Stage 1
              -> [2. Vigenere]     -> Stage 2
              -> [3. LFSR stream]  -> Stage 3 (bytes)
              -> [4. Vernam / OTP] -> Stage 4 Final (Hex)

    If vernam_key is None/empty, a random one-time key of the required length is generated.
    """
    trace = {}

    # 1. Playfair Cipher (first, so 'J' -> 'I' merging only affects the raw plaintext)
    c1, matrix, key_chars, pf_steps = encrypt_playfair(plaintext, key_playfair)
    trace["stage_1"] = {
        "name": "1. Playfair Cipher",
        "input": plaintext,
        "key": key_playfair,
        "output": c1,
        "details": f"Enkripsi Playfair selesai ({len(pf_steps)} digraph diproses, panjang {len(c1)})."
    }

    # 2. Vigenere Cipher
    c2, vig_steps = encrypt_vigenere(c1, key_vig)
    trace["stage_2"] = {
        "name": "2. Vigenère Cipher",
        "input": c1,
        "key": key_vig,
        "output": c2,
        "details": f"Enkripsi Vigenère selesai ({len(vig_steps)} karakter diproses)."
    }

    # 3. LFSR-based stream cipher
    c3_bytes, lfsr_steps, _ = lfsr_crypt_bytes(c2.encode("utf-8"), lfsr_seed, lfsr_n)
    trace["stage_3"] = {
        "name": "3. LFSR Stream Cipher",
        "input": c2,
        "key": f"seed={lfsr_seed}, register={lfsr_n} bit",
        "output": _hex(c3_bytes),
        "details": f"Enkripsi LFSR selesai ({len(lfsr_steps)} byte di-XOR dengan keystream {len(lfsr_steps) * 8} bit)."
    }

    # 4. Vernam Cipher (One-Time Pad)
    generated = not vernam_key
    if generated:
        vernam_key = generate_vernam_key(len(c3_bytes))
    c4_bytes, vn_steps = vernam_xor_bytes(c3_bytes, vernam_key.encode("utf-8"))
    final_hex = _hex(c4_bytes)
    trace["stage_4"] = {
        "name": "4. Vernam Cipher (One-Time Pad)",
        "input": _hex(c3_bytes),
        "key": vernam_key,
        "output": final_hex,
        "details": f"Enkripsi Vernam selesai ({len(vn_steps)} byte di-XOR dengan kunci OTP"
                   f"{' yang dibangkitkan otomatis' if generated else ''})."
    }
    trace["vernam_key"] = vernam_key
    trace["vernam_key_generated"] = generated

    return final_hex, trace


def super_decrypt(
    ciphertext: str,
    key_vig: str,
    key_playfair: str,
    lfsr_seed: str,
    lfsr_n: int,
    vernam_key: str
) -> Tuple[str, Dict[str, Any]]:
    """
    Executes inverse 4-layer sequential Super Decryption:
    Ciphertext (Hex) -> [1. Vernam Decrypt]   -> Stage 3 (bytes)
                     -> [2. LFSR Decrypt]     -> Stage 2
                     -> [3. Vigenere Decrypt] -> Stage 1
                     -> [4. Playfair Decrypt] -> Plaintext Asli
    """
    trace = {}

    try:
        cipher_bytes = bytes.fromhex("".join(ciphertext.split()))
    except ValueError:
        raise ValueError("Ciphertext harus berupa string heksadesimal yang valid.")

    # 1. Vernam Decrypt
    d1_bytes, vn_steps = vernam_xor_bytes(cipher_bytes, vernam_key.encode("utf-8"))
    trace["stage_1"] = {
        "name": "1. Vernam Decryption",
        "input": _hex(cipher_bytes),
        "key": vernam_key,
        "output": _hex(d1_bytes),
        "details": f"Dekripsi Vernam selesai ({len(vn_steps)} byte di-XOR kembali dengan kunci OTP)."
    }

    # 2. LFSR Decrypt
    d2_bytes, lfsr_steps, _ = lfsr_crypt_bytes(d1_bytes, lfsr_seed, lfsr_n)
    try:
        d2_text = d2_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Hasil dekripsi LFSR bukan teks valid (kunci Vernam atau seed LFSR kemungkinan salah).")
    trace["stage_2"] = {
        "name": "2. LFSR Decryption",
        "input": _hex(d1_bytes),
        "key": f"seed={lfsr_seed}, register={lfsr_n} bit",
        "output": d2_text,
        "details": f"Dekripsi LFSR selesai ({len(lfsr_steps)} byte, keystream identik dengan saat enkripsi)."
    }

    # 3. Vigenere Decrypt
    d3_text, vig_steps = decrypt_vigenere(d2_text, key_vig)
    trace["stage_3"] = {
        "name": "3. Vigenère Decryption",
        "input": d2_text,
        "key": key_vig,
        "output": d3_text,
        "details": f"Dekripsi Vigenère selesai ({len(vig_steps)} karakter dipulihkan)."
    }

    # 4. Playfair Decrypt
    d4_text, matrix, key_chars, pf_steps = decrypt_playfair(d3_text, key_playfair)
    trace["stage_4"] = {
        "name": "4. Playfair Decryption",
        "input": d3_text,
        "key": key_playfair,
        "output": d4_text,
        "details": f"Dekripsi Playfair selesai ({len(pf_steps)} digraph diproses)."
    }

    return d4_text, trace
