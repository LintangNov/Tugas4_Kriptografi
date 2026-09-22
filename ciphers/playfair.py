from typing import List, Dict, Tuple, Any, Set

def prepare_playfair_key(key: str) -> Tuple[List[List[str]], List[str]]:
    """
    Generates a 5x5 matrix from the key, replacing 'J' with 'I'.
    Returns (matrix_5x5, list_of_key_letters).
    """
    clean = []
    seen = set()
    for char in key.upper():
        if char.isalpha():
            c = 'I' if char == 'J' else char
            if c not in seen:
                seen.add(c)
                clean.append(c)
    
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Note: J is excluded
    matrix_letters = list(clean)
    for char in alphabet:
        if char not in seen:
            seen.add(char)
            matrix_letters.append(char)
            
    matrix = [matrix_letters[i*5:(i+1)*5] for i in range(5)]
    return matrix, clean

def find_position(matrix: List[List[str]], char: str) -> Tuple[int, int]:
    """Finds row and col coordinates of a character in the 5x5 matrix."""
    c = 'I' if char == 'J' else char
    for r in range(5):
        for col in range(5):
            if matrix[r][col] == c:
                return r, col
    raise ValueError(f"Karakter '{char}' tidak ditemukan di matriks Playfair.")

def prepare_text_for_playfair(text: str) -> List[Tuple[str, str]]:
    """
    Cleans text, replaces J with I, inserts 'X' between duplicates,
    and pads odd length with 'X' (or 'Z' if last char is 'X').
    Returns a list of 2-character pairs (digraphs).
    """
    filtered = []
    for ch in text.upper():
        if ch.isalpha():
            filtered.append('I' if ch == 'J' else ch)
            
    digraphs = []
    i = 0
    while i < len(filtered):
        c1 = filtered[i]
        if i + 1 < len(filtered):
            c2 = filtered[i + 1]
            if c1 == c2:
                # Same character in digraph, insert 'X' (or 'Z' if c1 is 'X')
                filler = 'Z' if c1 == 'X' else 'X'
                digraphs.append((c1, filler))
                i += 1
            else:
                digraphs.append((c1, c2))
                i += 2
        else:
            # Single character left at end, pad with 'X' (or 'Z' if c1 is 'X')
            filler = 'Z' if c1 == 'X' else 'X'
            digraphs.append((c1, filler))
            i += 1
            
    return digraphs

def encrypt_playfair(plaintext: str, key: str) -> Tuple[str, List[List[str]], List[str], List[Dict[str, Any]]]:
    """
    Encrypts plaintext using Playfair Cipher with step-by-step tracing.
    """
    matrix, key_chars = prepare_playfair_key(key)
    digraphs = prepare_text_for_playfair(plaintext)
    
    cipher_pairs = []
    steps = []
    
    for idx, (c1, c2) in enumerate(digraphs):
        r1, col1 = find_position(matrix, c1)
        r2, col2 = find_position(matrix, c2)
        
        if r1 == r2:
            # Same row: shift right circularly
            rule = "Baris Sama (Same Row)"
            rule_desc = "Kedua huruf berada di baris yang sama. Geser 1 kolom ke kanan secara sirkular."
            nr1, ncol1 = r1, (col1 + 1) % 5
            nr2, ncol2 = r2, (col2 + 1) % 5
        elif col1 == col2:
            # Same column: shift down circularly
            rule = "Kolom Sama (Same Column)"
            rule_desc = "Kedua huruf berada di kolom yang sama. Geser 1 baris ke bawah secara sirkular."
            nr1, ncol1 = (r1 + 1) % 5, col1
            nr2, ncol2 = (r2 + 1) % 5, col2
        else:
            # Rectangle: swap columns
            rule = "Persegi Empat (Rectangle)"
            rule_desc = "Membentuk persegi empat. Ambil huruf pada baris yang sama di sudut kolom pasangan."
            nr1, ncol1 = r1, col2
            nr2, ncol2 = r2, col1
            
        res1 = matrix[nr1][ncol1]
        res2 = matrix[nr2][ncol2]
        cipher_pairs.append(res1 + res2)
        
        steps.append({
            "pair_idx": idx + 1,
            "in_pair": f"{c1}{c2}",
            "c1": c1,
            "c2": c2,
            "pos1": (r1, col1),
            "pos2": (r2, col2),
            "rule": rule,
            "rule_desc": rule_desc,
            "new_pos1": (nr1, ncol1),
            "new_pos2": (nr2, ncol2),
            "out_pair": f"{res1}{res2}",
            "res1": res1,
            "res2": res2
        })
        
    return "".join(cipher_pairs), matrix, key_chars, steps

def decrypt_playfair(ciphertext: str, key: str) -> Tuple[str, List[List[str]], List[str], List[Dict[str, Any]]]:
    """
    Decrypts ciphertext using Playfair Cipher with step-by-step tracing.
    """
    matrix, key_chars = prepare_playfair_key(key)
    
    # Filter only alphabets for ciphertext
    clean_cipher = "".join([c.upper() for c in ciphertext if c.isalpha()])
    if len(clean_cipher) % 2 != 0:
        clean_cipher += 'X'
        
    digraphs = [(clean_cipher[i], clean_cipher[i+1]) for i in range(0, len(clean_cipher), 2)]
    
    plain_pairs = []
    steps = []
    
    for idx, (c1, c2) in enumerate(digraphs):
        r1, col1 = find_position(matrix, c1)
        r2, col2 = find_position(matrix, c2)
        
        if r1 == r2:
            # Same row: shift left circularly
            rule = "Baris Sama (Same Row)"
            rule_desc = "Kedua huruf berada di baris yang sama. Geser 1 kolom ke kiri secara sirkular."
            nr1, ncol1 = r1, (col1 - 1 + 5) % 5
            nr2, ncol2 = r2, (col2 - 1 + 5) % 5
        elif col1 == col2:
            # Same column: shift up circularly
            rule = "Kolom Sama (Same Column)"
            rule_desc = "Kedua huruf berada di kolom yang sama. Geser 1 baris ke atas secara sirkular."
            nr1, ncol1 = (r1 - 1 + 5) % 5, col1
            nr2, ncol2 = (r2 - 1 + 5) % 5, col2
        else:
            # Rectangle: swap columns
            rule = "Persegi Empat (Rectangle)"
            rule_desc = "Membentuk persegi empat. Ambil huruf pada baris yang sama di sudut kolom pasangan."
            nr1, ncol1 = r1, col2
            nr2, ncol2 = r2, col1
            
        res1 = matrix[nr1][ncol1]
        res2 = matrix[nr2][ncol2]
        plain_pairs.append(res1 + res2)
        
        steps.append({
            "pair_idx": idx + 1,
            "in_pair": f"{c1}{c2}",
            "c1": c1,
            "c2": c2,
            "pos1": (r1, col1),
            "pos2": (r2, col2),
            "rule": rule,
            "rule_desc": rule_desc,
            "new_pos1": (nr1, ncol1),
            "new_pos2": (nr2, ncol2),
            "out_pair": f"{res1}{res2}",
            "res1": res1,
            "res2": res2
        })
        
    return "".join(plain_pairs), matrix, key_chars, steps
