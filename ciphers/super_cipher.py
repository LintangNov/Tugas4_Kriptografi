from typing import Dict, Any, Tuple
from ciphers.vigenere import encrypt_vigenere, decrypt_vigenere
from ciphers.playfair import encrypt_playfair, decrypt_playfair
from ciphers.aes_cipher import encrypt_aes, decrypt_aes
from ciphers.rsa_cipher import generate_rsa_keys, encrypt_rsa_char_by_char, decrypt_rsa_char_by_char

def super_encrypt(
    plaintext: str,
    key_vig: str,
    key_playfair: str,
    key_aes: str,
    rsa_p: int,
    rsa_q: int,
    rsa_e: int = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Executes 4-layer sequential Super Encryption:
    Plaintext -> [1. Vigenere] -> Stage 1
              -> [2. Playfair] -> Stage 2
              -> [3. AES-128]  -> Stage 3 (Base64)
              -> [4. RSA]      -> Stage 4 Final (Numeric Sequence)
    """
    trace = {}
    
    # 1. Vigenere Cipher
    c1, vig_steps = encrypt_vigenere(plaintext, key_vig)
    trace["stage_1"] = {
        "name": "1. Vigenère Cipher",
        "input": plaintext,
        "key": key_vig,
        "output": c1,
        "details": f"Enkripsi Vigenère selesai ({len(vig_steps)} karakter diproses)."
    }
    
    # 2. Playfair Cipher
    c2, matrix, key_chars, pf_steps = encrypt_playfair(c1, key_playfair)
    trace["stage_2"] = {
        "name": "2. Playfair Cipher",
        "input": c1,
        "key": key_playfair,
        "output": c2,
        "details": f"Enkripsi Playfair selesai ({len(pf_steps)} digraph diproses, panjang {len(c2)})."
    }
    
    # 3. AES-128 Cipher
    b64_cipher, hex_cipher, aes_trace = encrypt_aes(c2, key_aes)
    trace["stage_3"] = {
        "name": "3. AES-128 Modern",
        "input": c2,
        "key": key_aes,
        "output": b64_cipher,
        "output_hex": hex_cipher,
        "details": f"Enkripsi AES selesai (Padded {aes_trace['padded_len']} byte, Base64 output)."
    }
    
    # 4. RSA Cipher
    rsa_keys = generate_rsa_keys(rsa_p, rsa_q, rsa_e)
    e = rsa_keys["e"]
    n = rsa_keys["n"]
    cipher_ints, rsa_str, rsa_steps = encrypt_rsa_char_by_char(b64_cipher, e, n)
    trace["stage_4"] = {
        "name": "4. RSA Asimetris",
        "input": b64_cipher,
        "key": f"e={e}, n={n}",
        "output": rsa_str,
        "details": f"Enkripsi RSA selesai ({len(rsa_steps)} karakter ASCII dienkripsi menjadi integer modular)."
    }
    trace["rsa_keys"] = rsa_keys

    return rsa_str, trace

def super_decrypt(
    ciphertext: str,
    key_vig: str,
    key_playfair: str,
    key_aes: str,
    rsa_p: int,
    rsa_q: int,
    rsa_e: int = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Executes inverse 4-layer sequential Super Decryption:
    Ciphertext -> [1. RSA Decrypt]      -> Stage 3 (Base64)
               -> [2. AES-128 Decrypt]  -> Stage 2
               -> [3. Playfair Decrypt] -> Stage 1
               -> [4. Vigenere Decrypt] -> Plaintext Asli
    """
    trace = {}
    
    # 1. RSA Decrypt
    rsa_keys = generate_rsa_keys(rsa_p, rsa_q, rsa_e)
    d = rsa_keys["d"]
    n = rsa_keys["n"]
    dec_rsa_b64, rsa_steps = decrypt_rsa_char_by_char(ciphertext, d, n)
    trace["stage_1"] = {
        "name": "1. RSA Decryption",
        "input": ciphertext[:80] + ("..." if len(ciphertext) > 80 else ""),
        "key": f"d={d}, n={n}",
        "output": dec_rsa_b64,
        "details": f"Dekripsi RSA selesai ({len(rsa_steps)} blok integer dipulihkan ke Base64)."
    }
    
    # 2. AES Decrypt
    dec_aes_text, aes_trace = decrypt_aes(dec_rsa_b64, key_aes, is_base64=True)
    trace["stage_2"] = {
        "name": "2. AES-128 Decryption",
        "input": dec_rsa_b64,
        "key": key_aes,
        "output": dec_aes_text,
        "details": f"Dekripsi AES selesai (Padding {aes_trace['padding_removed']} byte dihapus)."
    }
    
    # 3. Playfair Decrypt
    dec_pf_text, matrix, key_chars, pf_steps = decrypt_playfair(dec_aes_text, key_playfair)
    trace["stage_3"] = {
        "name": "3. Playfair Decryption",
        "input": dec_aes_text,
        "key": key_playfair,
        "output": dec_pf_text,
        "details": f"Dekripsi Playfair selesai ({len(pf_steps)} digraph diproses)."
    }
    
    # 4. Vigenere Decrypt
    dec_vig_text, vig_steps = decrypt_vigenere(dec_pf_text, key_vig)
    trace["stage_4"] = {
        "name": "4. Vigenère Decryption",
        "input": dec_pf_text,
        "key": key_vig,
        "output": dec_vig_text,
        "details": f"Dekripsi Vigenère selesai ({len(vig_steps)} karakter dipulihkan)."
    }
    trace["rsa_keys"] = rsa_keys
    
    return dec_vig_text, trace
