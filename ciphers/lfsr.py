from typing import List, Dict, Tuple, Any

# Maximal-length feedback polynomials (tap positions counted from the input side, 1..n).
# x^4+x^3+1, x^8+x^6+x^5+x^4+1, x^16+x^14+x^13+x^11+1
LFSR_TAPS: Dict[int, List[int]] = {
    4: [4, 3],
    8: [8, 6, 5, 4],
    16: [16, 14, 13, 11],
}


def polynomial_str(n: int) -> str:
    terms = [f"x^{t}" for t in LFSR_TAPS[n]] + ["1"]
    return " + ".join(terms)


def parse_seed(seed_bits: str, n: int) -> int:
    """Validates an n-bit binary seed string and returns it as an integer."""
    if n not in LFSR_TAPS:
        raise ValueError(f"Panjang register {n} tidak didukung.")
    s = seed_bits.strip()
    if len(s) != n or any(c not in "01" for c in s):
        raise ValueError(f"Seed harus berupa {n} digit biner (0/1).")
    seed = int(s, 2)
    if seed == 0:
        raise ValueError("Seed tidak boleh semua nol (register akan macet di state 0).")
    return seed


def lfsr_clock(state: int, n: int) -> Tuple[int, int, int]:
    """
    One clock of a Fibonacci LFSR (shift right).
    Output bit = LSB. Feedback = XOR of tap bits, inserted at the MSB.
    Tap position t maps to bit index (n - t).
    Returns (new_state, output_bit, feedback_bit).
    """
    fb = 0
    for t in LFSR_TAPS[n]:
        fb ^= (state >> (n - t)) & 1
    out = state & 1
    new_state = (state >> 1) | (fb << (n - 1))
    return new_state, out, fb


def lfsr_clock_trace(seed: int, n: int, clocks: int) -> List[Dict[str, Any]]:
    """Records register state, feedback and output bit for the first `clocks` clocks."""
    rows = []
    state = seed
    for i in range(clocks):
        new_state, out, fb = lfsr_clock(state, n)
        tap_bits = " XOR ".join(str((state >> (n - t)) & 1) for t in LFSR_TAPS[n])
        rows.append({
            "clock": i + 1,
            "state": f"{state:0{n}b}",
            "feedback": f"{tap_bits} = {fb}",
            "output": out,
            "next_state": f"{new_state:0{n}b}",
        })
        state = new_state
    return rows


def lfsr_keystream_bytes(seed: int, n: int, length: int) -> bytes:
    """Generates `length` keystream bytes (8 clocks per byte, first output bit = MSB)."""
    state = seed
    out = bytearray()
    for _ in range(length):
        byte = 0
        for _ in range(8):
            state, bit, _fb = lfsr_clock(state, n)
            byte = (byte << 1) | bit
        out.append(byte)
    return bytes(out)


def _printable(b: int) -> str:
    return chr(b) if 32 <= b < 127 else "."


def lfsr_crypt_bytes(data: bytes, seed_bits: str, n: int) -> Tuple[bytes, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Stream cipher: C_i = P_i XOR KS_i. Symmetric, so it also decrypts.
    Returns (output_bytes, byte_steps, clock_trace_of_first_24_clocks).
    """
    seed = parse_seed(seed_bits, n)
    ks = lfsr_keystream_bytes(seed, n, len(data))
    out = bytearray()
    steps = []
    for i, (d, k) in enumerate(zip(data, ks)):
        x = d ^ k
        out.append(x)
        steps.append({
            "index": i + 1,
            "in_char": _printable(d),
            "in_bin": f"{d:08b}",
            "ks_bin": f"{k:08b}",
            "ks_hex": f"{k:02X}",
            "xor_bin": f"{x:08b}",
            "out_hex": f"{x:02X}",
            "out_char": _printable(x),
        })
    trace = lfsr_clock_trace(seed, n, min(24, len(data) * 8))
    return bytes(out), steps, trace


def encrypt_lfsr(plaintext: str, seed_bits: str, n: int):
    """Encrypts text. Returns (ciphertext_hex, byte_steps, clock_trace)."""
    cipher, steps, trace = lfsr_crypt_bytes(plaintext.encode("utf-8"), seed_bits, n)
    return cipher.hex().upper(), steps, trace


def decrypt_lfsr(cipher_hex: str, seed_bits: str, n: int):
    """Decrypts hex ciphertext. Returns (plaintext, byte_steps, clock_trace)."""
    try:
        cipher = bytes.fromhex("".join(cipher_hex.split()))
    except ValueError:
        raise ValueError("Ciphertext LFSR harus berupa string heksadesimal yang valid.")
    plain, steps, trace = lfsr_crypt_bytes(cipher, seed_bits, n)
    try:
        return plain.decode("utf-8"), steps, trace
    except UnicodeDecodeError:
        raise ValueError("Hasil dekripsi bukan teks UTF-8 yang valid (seed kemungkinan salah).")
