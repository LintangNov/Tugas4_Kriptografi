import streamlit as st
import pandas as pd
from ciphers.lfsr import LFSR_TAPS, polynomial_str, encrypt_lfsr, decrypt_lfsr

st.set_page_config(
    page_title="LFSR Stream Cipher",
    layout="wide"
)

st.header("LFSR-based Stream Cipher (Modern - Stream Simetris)")
st.write(
    "Sandi aliran yang membangkitkan keystream pseudo-acak dari Linear Feedback Shift Register (LFSR), "
    "lalu meng-XOR-kan keystream tersebut dengan plaintext."
)

DEFAULT_SEEDS = {4: "1001", 8: "10110001", 16: "1010110011100001"}


def register_inputs(prefix: str):
    """Shared register-size and seed widgets for both tabs."""
    n = st.selectbox("Panjang Register (bit)", list(LFSR_TAPS.keys()), index=1, key=f"{prefix}_n")
    seed = st.text_input(f"Seed awal ({n} digit biner, tidak boleh nol semua)", value=DEFAULT_SEEDS[n], key=f"{prefix}_seed_{n}")
    st.caption(f"Polinomial umpan balik: {polynomial_str(n)} | Tap: {LFSR_TAPS[n]} | Periode maksimum: {2**n - 1}")
    return n, seed


def show_clock_trace(trace):
    st.write("**Jejak clock register (maksimal 24 clock pertama):**")
    st.dataframe(pd.DataFrame([{
        "Clock": t["clock"],
        "State Register": t["state"],
        "Feedback (XOR tap)": t["feedback"],
        "Bit Output": t["output"],
        "State Berikutnya": t["next_state"],
    } for t in trace]), use_container_width=True)


tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

# ----------------- TAB ENKRIPSI -----------------
with tab_enc:
    col1, col2 = st.columns([3, 2])

    with col1:
        enc_plain = st.text_area(
            "Plaintext (Teks Asli)",
            value="KRIPTOGRAFI",
            height=120,
            key="lfsr_enc_plain"
        )

    with col2:
        enc_n, enc_seed = register_inputs("lfsr_enc")
        st.info("Rumus: C_i = P_i XOR KS_i. Feedback = XOR bit-bit tap, di-shift masuk dari kiri, output = bit paling kanan.")

    if st.button("Proses Enkripsi", key="btn_enc_lfsr", use_container_width=True):
        if not enc_plain:
            st.warning("Input plaintext tidak boleh kosong.")
        else:
            try:
                cipher_hex, steps, trace = encrypt_lfsr(enc_plain, enc_seed, enc_n)

                st.subheader("Hasil Enkripsi (Ciphertext Heksadesimal)")
                st.code(cipher_hex, language="text")

                st.divider()
                st.subheader("Visualisasi Proses Algoritma")

                m1, m2, m3 = st.columns(3)
                m1.metric("Jumlah Byte", len(steps))
                m2.metric("Total Clock", len(steps) * 8)
                m3.metric("Panjang Register", f"{enc_n} bit")

                show_clock_trace(trace)

                st.write("**XOR plaintext dengan keystream per byte:**")
                st.dataframe(pd.DataFrame([{
                    "No": s["index"],
                    "Karakter Plain": s["in_char"],
                    "Biner P": s["in_bin"],
                    "Keystream (Biner)": s["ks_bin"],
                    "Keystream (Hex)": s["ks_hex"],
                    "P XOR KS": s["xor_bin"],
                    "Hex Cipher": s["out_hex"],
                } for s in steps]), use_container_width=True)

            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")

# ----------------- TAB DEKRIPSI -----------------
with tab_dec:
    col_d1, col_d2 = st.columns([3, 2])

    with col_d1:
        dec_cipher = st.text_area(
            "Ciphertext (Heksadesimal)",
            value="",
            placeholder="Tempelkan ciphertext hex hasil enkripsi di sini...",
            height=120,
            key="lfsr_dec_cipher"
        )

    with col_d2:
        dec_n, dec_seed = register_inputs("lfsr_dec")
        st.info("Dekripsi membangkitkan keystream yang identik dari seed yang sama, lalu XOR ulang: P_i = C_i XOR KS_i.")

    if st.button("Proses Dekripsi", key="btn_dec_lfsr", use_container_width=True):
        if not dec_cipher.strip():
            st.warning("Input ciphertext tidak boleh kosong.")
        else:
            try:
                plain, steps, trace = decrypt_lfsr(dec_cipher, dec_seed, dec_n)

                st.subheader("Hasil Dekripsi (Plaintext)")
                st.code(plain, language="text")

                st.divider()
                st.subheader("Visualisasi Proses Pembalikan")
                show_clock_trace(trace)

                st.write("**XOR ciphertext dengan keystream per byte:**")
                st.dataframe(pd.DataFrame([{
                    "No": s["index"],
                    "Biner C": s["in_bin"],
                    "Keystream (Biner)": s["ks_bin"],
                    "Keystream (Hex)": s["ks_hex"],
                    "C XOR KS": s["xor_bin"],
                    "Karakter Plain": s["out_char"],
                } for s in steps]), use_container_width=True)

            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")
