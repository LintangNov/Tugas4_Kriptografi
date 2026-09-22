import math
from typing import List, Dict, Tuple, Any

def is_prime(num: int) -> bool:
    """Checks if a number is prime."""
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e: int, phi: int) -> int:
    """
    Computes modular multiplicative inverse d such that (e * d) % phi == 1.
    """
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError(f"Invers modular tidak ditemukan karena gcd({e}, {phi}) = {gcd_val} != 1.")
    return (x % phi + phi) % phi

def get_possible_e_values(phi: int, limit: int = 10) -> List[int]:
    """Returns candidate values of e that are coprime with phi."""
    candidates = []
    common_e = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 65537]
    for val in common_e:
        if 1 < val < phi and math.gcd(val, phi) == 1:
            candidates.append(val)
    # If not enough, search sequentially
    for val in range(3, phi, 2):
        if len(candidates) >= limit:
            break
        if val not in candidates and math.gcd(val, phi) == 1:
            candidates.append(val)
    return candidates

def generate_rsa_keys(p: int, q: int, e: int = None) -> Dict[str, Any]:
    """
    Generates RSA public and private key parameters with step-by-step mathematical tracing.
    """
    if not is_prime(p):
        raise ValueError(f"Nilai p = {p} bukan bilangan prima.")
    if not is_prime(q):
        raise ValueError(f"Nilai q = {q} bukan bilangan prima.")
    if p == q:
        raise ValueError("Nilai p dan q tidak boleh bernilai sama.")
        
    n = p * q
    phi = (p - 1) * (q - 1)
    
    valid_e_list = get_possible_e_values(phi)
    if not valid_e_list:
        raise ValueError(f"Tidak dapat menemukan nilai e yang valid untuk phi = {phi}.")
        
    if e is None:
        e = valid_e_list[0]
    else:
        if not (1 < e < phi):
            raise ValueError(f"Nilai e harus berada di antara 1 dan phi ({phi}).")
        if math.gcd(e, phi) != 1:
            raise ValueError(f"Nilai e ({e}) tidak relatif prima dengan phi ({phi}). gcd = {math.gcd(e, phi)}.")
            
    d = mod_inverse(e, phi)
    
    return {
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d,
        "public_key": (e, n),
        "private_key": (d, n),
        "valid_e_list": valid_e_list
    }

def encrypt_rsa_char_by_char(plaintext: str, e: int, n: int) -> Tuple[List[int], str, List[Dict[str, Any]]]:
    """
    Encrypts plaintext character by character using C = (M^e) mod n.
    Returns (list_of_cipher_ints, formatted_cipher_str, steps).
    """
    cipher_ints = []
    steps = []
    
    for idx, char in enumerate(plaintext):
        m = ord(char)
        if m >= n:
            raise ValueError(
                f"Nilai ASCII karakter '{char}' ({m}) >= n ({n}). "
                f"Pilih bilangan prima p dan q yang lebih besar sehingga n > {m}."
            )
        # Modular exponentiation
        c = pow(m, e, n)
        cipher_ints.append(c)
        steps.append({
            "index": idx + 1,
            "char": char,
            "m_val": m,
            "formula": f"{m}^{e} mod {n}",
            "c_val": c
        })
        
    formatted_str = " ".join(map(str, cipher_ints))
    return cipher_ints, formatted_str, steps

def decrypt_rsa_char_by_char(cipher_input: str, d: int, n: int) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Decrypts space-separated or comma-separated integer ciphertext using M = (C^d) mod n.
    Returns (plaintext, steps).
    """
    # Clean and parse tokens
    raw_tokens = cipher_input.replace(",", " ").split()
    if not raw_tokens:
        raise ValueError("Ciphertext RSA kosong.")
        
    try:
        cipher_ints = [int(tok) for tok in raw_tokens]
    except ValueError:
        raise ValueError("Ciphertext RSA harus berupa deretan angka integer yang dipisahkan spasi atau koma.")
        
    chars = []
    steps = []
    
    for idx, c in enumerate(cipher_ints):
        m = pow(c, d, n)
        try:
            char = chr(m)
        except Exception:
            char = "?"
            
        chars.append(char)
        steps.append({
            "index": idx + 1,
            "c_val": c,
            "formula": f"{c}^{d} mod {n}",
            "m_val": m,
            "char": char
        })
        
    plaintext = "".join(chars)
    return plaintext, steps
