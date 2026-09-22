from typing import List, Dict, Tuple, Any

def clean_key(key: str) -> str:
    """Removes non-alphabetic characters and converts to uppercase."""
    return "".join([c.upper() for c in key if c.isalpha()])

def encrypt_vigenere(plaintext: str, key: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Encrypts plaintext using Vigenere Cipher with full step-by-step tracing.
    
    Formula:
    C_i = (P_i + K_i) mod 26
    """
    cleaned_key = clean_key(key)
    if not cleaned_key:
        raise ValueError("Kunci Vigenere harus mengandung setidaknya satu huruf alfabet.")

    ciphertext_chars = []
    steps = []
    key_len = len(cleaned_key)
    key_idx = 0

    for i, char in enumerate(plaintext):
        if char.isalpha():
            is_upper = char.isupper()
            p_val = ord(char.upper()) - ord('A')
            k_char = cleaned_key[key_idx % key_len]
            k_val = ord(k_char) - ord('A')
            c_val = (p_val + k_val) % 26
            c_char = chr(c_val + ord('A'))
            
            if not is_upper:
                c_char = c_char.lower()
                
            ciphertext_chars.append(c_char)
            steps.append({
                "index": i + 1,
                "plain_char": char,
                "p_val": p_val,
                "key_char": k_char,
                "k_val": k_val,
                "shift": f"+{k_val}",
                "calc": f"({p_val} + {k_val}) mod 26 = {c_val}",
                "result_char": c_char
            })
            key_idx += 1
        else:
            ciphertext_chars.append(char)
            steps.append({
                "index": i + 1,
                "plain_char": char,
                "p_val": "-",
                "key_char": "-",
                "k_val": "-",
                "shift": "0",
                "calc": "Karakter non-alfabet dipertahankan",
                "result_char": char
            })

    return "".join(ciphertext_chars), steps

def decrypt_vigenere(ciphertext: str, key: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Decrypts ciphertext using Vigenere Cipher with full step-by-step tracing.
    
    Formula:
    P_i = (C_i - K_i + 26) mod 26
    """
    cleaned_key = clean_key(key)
    if not cleaned_key:
        raise ValueError("Kunci Vigenere harus mengandung setidaknya satu huruf alfabet.")

    plaintext_chars = []
    steps = []
    key_len = len(cleaned_key)
    key_idx = 0

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            is_upper = char.isupper()
            c_val = ord(char.upper()) - ord('A')
            k_char = cleaned_key[key_idx % key_len]
            k_val = ord(k_char) - ord('A')
            p_val = (c_val - k_val + 26) % 26
            p_char = chr(p_val + ord('A'))
            
            if not is_upper:
                p_char = p_char.lower()
                
            plaintext_chars.append(p_char)
            steps.append({
                "index": i + 1,
                "cipher_char": char,
                "c_val": c_val,
                "key_char": k_char,
                "k_val": k_val,
                "shift": f"-{k_val}",
                "calc": f"({c_val} - {k_val} + 26) mod 26 = {p_val}",
                "result_char": p_char
            })
            key_idx += 1
        else:
            plaintext_chars.append(char)
            steps.append({
                "index": i + 1,
                "cipher_char": char,
                "c_val": "-",
                "key_char": "-",
                "k_val": "-",
                "shift": "0",
                "calc": "Karakter non-alfabet dipertahankan",
                "result_char": char
            })

    return "".join(plaintext_chars), steps
