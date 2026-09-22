import streamlit as st
import pandas as pd
from ciphers.vigenere import encrypt_vigenere, decrypt_vigenere

st.set_page_config(
    page_title="Vigenère Cipher",
    layout="wide"
)

st.header("Vigenère Cipher (Klasik - Polialfabetik)")
st.write(
    "Sandi substitusi polialfabetik yang menggunakan deretan sandi Caesar berdasarkan huruf-huruf pada kata kunci."
)

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

# ----------------- TAB ENKRIPSI -----------------
with tab_enc:
    col_input1, col_input2 = st.columns([3, 2])
    
    with col_input1:
        enc_plaintext = st.text_area(
            "Plaintext (Teks Asli)",
            value="KRIPTOGRAFI SEMESTER LIMA",
            height=120,
            key="vigenere_enc_plain"
        )
        
    with col_input2:
        enc_key = st.text_input(
            "Kunci (Key)",
            value="KUNCI",
            key="vigenere_enc_key"
        )
        st.info("Rumus enkripsi: C_i = (P_i + K_i) mod 26. Karakter non-alfabet tetap dipertahankan.")

    if st.button("Proses Enkripsi", key="btn_enc_vigenere", use_container_width=True):
        if not enc_plaintext.strip():
            st.warning("Input plaintext tidak boleh kosong.")
        elif not enc_key.strip():
            st.warning("Kunci tidak boleh kosong.")
        else:
            try:
                ciphertext, steps = encrypt_vigenere(enc_plaintext, enc_key)
                
                st.subheader("Hasil Enkripsi (Ciphertext)")
                st.code(ciphertext, language="text")
                
                st.divider()
                st.subheader("Visualisasi Proses Algoritma")
                
                m1, m2, m3 = st.columns(3)
                alpha_count = sum(1 for s in steps if s["p_val"] != "-")
                m1.metric("Total Karakter", len(steps))
                m2.metric("Karakter Alfabet", alpha_count)
                m3.metric("Panjang Kunci Efektif", len([c for c in enc_key if c.isalpha()]))
                
                table_rows = []
                for s in steps:
                    table_rows.append({
                        "No": s["index"],
                        "Karakter Plain": s["plain_char"],
                        "Nilai P": s["p_val"],
                        "Karakter Kunci": s["key_char"],
                        "Nilai K": s["k_val"],
                        "Pergeseran": s["shift"],
                        "Perhitungan": s["calc"],
                        "Karakter Cipher": s["result_char"]
                    })
                
                df_steps = pd.DataFrame(table_rows)
                st.dataframe(df_steps, use_container_width=True)
                
            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")

# ----------------- TAB DEKRIPSI -----------------
with tab_dec:
    col_dec1, col_dec2 = st.columns([3, 2])
    
    with col_dec1:
        dec_ciphertext = st.text_area(
            "Ciphertext (Teks Sandi)",
            value="",
            placeholder="Masukkan ciphertext di sini...",
            height=120,
            key="vigenere_dec_cipher"
        )
        
    with col_dec2:
        dec_key = st.text_input(
            "Kunci (Key)",
            value="KUNCI",
            key="vigenere_dec_key"
        )
        st.info("Rumus dekripsi: P_i = (C_i - K_i + 26) mod 26.")

    if st.button("Proses Dekripsi", key="btn_dec_vigenere", use_container_width=True):
        if not dec_ciphertext.strip():
            st.warning("Input ciphertext tidak boleh kosong.")
        elif not dec_key.strip():
            st.warning("Kunci tidak boleh kosong.")
        else:
            try:
                plaintext_res, steps = decrypt_vigenere(dec_ciphertext, dec_key)
                
                st.subheader("Hasil Dekripsi (Plaintext)")
                st.code(plaintext_res, language="text")
                
                st.divider()
                st.subheader("Visualisasi Proses Pembalikan")
                
                table_rows = []
                for s in steps:
                    table_rows.append({
                        "No": s["index"],
                        "Karakter Cipher": s["cipher_char"],
                        "Nilai C": s["c_val"],
                        "Karakter Kunci": s["key_char"],
                        "Nilai K": s["k_val"],
                        "Pergeseran": s["shift"],
                        "Perhitungan": s["calc"],
                        "Karakter Plain": s["result_char"]
                    })
                
                df_dec = pd.DataFrame(table_rows)
                st.dataframe(df_dec, use_container_width=True)
                
            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")
