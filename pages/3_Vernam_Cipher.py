import streamlit as st
import pandas as pd
from ciphers.vernam import encrypt_vernam, decrypt_vernam, generate_vernam_key

st.set_page_config(
    page_title="Vernam Cipher",
    layout="wide"
)

st.header("Vernam Cipher / One-Time Pad (Modern - Stream Simetris)")
st.write(
    "Sandi aliran yang meng-XOR setiap bit plaintext dengan bit kunci acak yang panjangnya "
    "sama persis dengan pesan dan hanya dipakai sekali."
)

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

# ----------------- TAB ENKRIPSI -----------------
with tab_enc:
    col1, col2 = st.columns([3, 2])

    with col1:
        enc_plain = st.text_area(
            "Plaintext (Teks Asli)",
            value="KRIPTOGRAFI",
            height=120,
            key="vernam_enc_plain"
        )

    with col2:
        auto_key = st.checkbox("Bangkitkan kunci acak otomatis", value=True, key="vernam_auto_key")
        enc_key = st.text_input(
            "Kunci OTP (panjang harus sama dengan plaintext)",
            value="",
            disabled=auto_key,
            key="vernam_enc_key"
        )
        st.info("Rumus: C_i = P_i XOR K_i. Kunci harus acak, sepanjang pesan, dan tidak dipakai ulang.")

    if st.button("Proses Enkripsi", key="btn_enc_vernam", use_container_width=True):
        if not enc_plain:
            st.warning("Input plaintext tidak boleh kosong.")
        else:
            try:
                key_used = generate_vernam_key(len(enc_plain.encode("utf-8"))) if auto_key else enc_key
                cipher_hex, steps = encrypt_vernam(enc_plain, key_used)

                st.subheader("Hasil Enkripsi (Ciphertext Heksadesimal)")
                st.code(cipher_hex, language="text")
                st.write("**Kunci OTP yang dipakai (simpan untuk dekripsi):**")
                st.code(key_used, language="text")

                st.divider()
                st.subheader("Visualisasi Proses Algoritma (XOR per Byte)")

                m1, m2 = st.columns(2)
                m1.metric("Panjang Pesan (byte)", len(steps))
                m2.metric("Panjang Kunci (byte)", len(key_used.encode("utf-8")))

                rows = [{
                    "No": s["index"],
                    "Karakter Plain": s["in_char"],
                    "ASCII P": s["in_dec"],
                    "Biner P": s["in_bin"],
                    "Karakter Kunci": s["key_char"],
                    "Biner K": s["key_bin"],
                    "P XOR K": s["xor_bin"],
                    "Hex Cipher": s["out_hex"],
                } for s in steps]
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

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
            key="vernam_dec_cipher"
        )

    with col_d2:
        dec_key = st.text_input("Kunci OTP", value="", key="vernam_dec_key")
        st.info("Dekripsi memakai operasi yang sama: P_i = C_i XOR K_i (XOR adalah inversnya sendiri).")

    if st.button("Proses Dekripsi", key="btn_dec_vernam", use_container_width=True):
        if not dec_cipher.strip():
            st.warning("Input ciphertext tidak boleh kosong.")
        elif not dec_key:
            st.warning("Kunci tidak boleh kosong.")
        else:
            try:
                plain, steps = decrypt_vernam(dec_cipher, dec_key)

                st.subheader("Hasil Dekripsi (Plaintext)")
                st.code(plain, language="text")

                st.divider()
                st.subheader("Visualisasi Proses Pembalikan")
                rows = [{
                    "No": s["index"],
                    "Hex Cipher": f"{s['in_dec']:02X}",
                    "Biner C": s["in_bin"],
                    "Karakter Kunci": s["key_char"],
                    "Biner K": s["key_bin"],
                    "C XOR K": s["xor_bin"],
                    "ASCII P": s["out_dec"],
                    "Karakter Plain": s["out_char"],
                } for s in steps]
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")
