import streamlit as st
import pandas as pd
from ciphers.aes_cipher import encrypt_aes, decrypt_aes
from utils.ui import format_aes_state_dataframe

st.set_page_config(
    page_title="AES Cipher",
    layout="wide"
)

st.header("Advanced Encryption Standard (AES)")
st.write(
    "Standar enkripsi blok simetris FIPS PUB 197 dengan ukuran blok 128-bit dan kunci 128-bit (10 round)."
)

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

# ----------------- TAB ENKRIPSI -----------------
with tab_enc:
    col_in1, col_in2 = st.columns([3, 2])
    
    with col_in1:
        enc_plaintext = st.text_area(
            "Plaintext (Teks Masukan)",
            value="Sistem Keamanan Data Berbasis Kriptografi Modern",
            height=120,
            key="aes_enc_plain"
        )
        
    with col_in2:
        enc_key = st.text_input(
            "Kunci Simetris (16 Karakter)",
            value="KunciRahasia1234",
            max_chars=16,
            key="aes_enc_key"
        )
        st.info("Kunci AES-128 memerlukan tepat 16 byte (128 bit). Mode yang digunakan: ECB dengan PKCS#7 padding.")

    if st.button("Proses Enkripsi AES", key="btn_enc_aes", use_container_width=True):
        if not enc_plaintext.strip():
            st.warning("Plaintext tidak boleh kosong.")
        elif not enc_key.strip():
            st.warning("Kunci simetris tidak boleh kosong.")
        else:
            try:
                b64_res, hex_res, trace = encrypt_aes(enc_plaintext, enc_key)
                
                st.subheader("Hasil Enkripsi")
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.write("**Format Base64:**")
                    st.code(b64_res, language="text")
                with col_res2:
                    st.write("**Format Heksadesimal (Hex):**")
                    st.code(hex_res, language="text")
                    
                st.divider()
                st.subheader("Visualisasi Tahapan Algoritma AES (Blok 1)")
                
                # Tahap 1: Padding PKCS#7
                st.write("**Tahap 1: PKCS#7 Padding**")
                p1, p2, p3 = st.columns(3)
                p1.metric("Panjang Awal (Byte)", trace["raw_len"])
                p2.metric("Padding Ditambahkan", trace["padding_added"])
                p3.metric("Panjang Setelah Padding", trace["padded_len"])
                st.write("Byte setelah padding (Hex):")
                st.code(trace["padded_bytes_hex"], language="text")
                
                # Tahap 2: Key Expansion
                st.write("**Tahap 2: Key Expansion (Round Keys)**")
                b_trace = trace["block_trace"]
                rkeys = b_trace["round_keys"]
                
                rk1, rk2 = st.columns(2)
                with rk1:
                    st.write("**Round Key 0 (Kunci Awal):**")
                    st.code(rkeys[0], language="text")
                with rk2:
                    st.write("**Round Key 10 (Kunci Terakhir):**")
                    st.code(rkeys[10], language="text")
                    
                with st.expander("Daftar Lengkap 11 Round Key"):
                    df_rk = pd.DataFrame({
                        "Round": [f"Round {i}" for i in range(11)],
                        "Kunci (16 Byte Hex)": rkeys
                    })
                    st.dataframe(df_rk, use_container_width=True)
                    
                # Tahap 3: State Matrix 4x4
                st.write("**Tahap 3: Visualisasi State Matrix 4x4 (Blok Pertama)**")
                st.write(f"Blok input 16-byte: `0x{b_trace['first_block_hex']}`")
                
                with st.expander("Pre-Round (Initial AddRoundKey)", expanded=True):
                    col_pr1, col_pr2 = st.columns(2)
                    with col_pr1:
                        st.write("State Awal (Input Block 4x4):")
                        st.dataframe(format_aes_state_dataframe(b_trace["initial_state"]), use_container_width=True)
                    with col_pr2:
                        st.write("State Setelah AddRoundKey (Kunci 0):")
                        st.dataframe(format_aes_state_dataframe(b_trace["pre_round_state"]), use_container_width=True)
                    st.caption("State awal di-XOR dengan Round Key 0.")

                with st.expander("Round 1 Transformations", expanded=True):
                    r1 = b_trace["round_1"]
                    r_c1, r_c2 = st.columns(2)
                    with r_c1:
                        st.write("1. SubBytes (Substitusi S-Box):")
                        st.dataframe(format_aes_state_dataframe(r1["sub_bytes"]), use_container_width=True)
                        st.write("3. MixColumns (Perkalian Galois Field):")
                        st.dataframe(format_aes_state_dataframe(r1["mix_columns"]), use_container_width=True)
                    with r_c2:
                        st.write("2. ShiftRows (Pergeseran Baris Siklis):")
                        st.dataframe(format_aes_state_dataframe(r1["shift_rows"]), use_container_width=True)
                        st.write("4. AddRoundKey (XOR Round Key 1):")
                        st.dataframe(format_aes_state_dataframe(r1["add_round_key"]), use_container_width=True)

            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")

# ----------------- TAB DEKRIPSI -----------------
with tab_dec:
    col_d1, col_d2 = st.columns([3, 2])
    
    with col_d1:
        dec_cipher_input = st.text_area(
            "Ciphertext Masukan",
            value="",
            placeholder="Tempelkan ciphertext Base64 atau Hex di sini...",
            height=120,
            key="aes_dec_input"
        )
        dec_format = st.radio(
            "Format Ciphertext:",
            ["Base64", "Heksadesimal (Hex)"],
            horizontal=True,
            key="aes_dec_fmt"
        )
        
    with col_d2:
        dec_key = st.text_input(
            "Kunci Simetris (16 Karakter)",
            value="KunciRahasia1234",
            max_chars=16,
            key="aes_dec_key"
        )
        st.info("Kunci harus sama persis dengan yang digunakan saat enkripsi.")

    if st.button("Proses Dekripsi AES", key="btn_dec_aes", use_container_width=True):
        if not dec_cipher_input.strip():
            st.warning("Ciphertext masukan tidak boleh kosong.")
        elif not dec_key.strip():
            st.warning("Kunci simetris tidak boleh kosong.")
        else:
            try:
                is_b64 = (dec_format == "Base64")
                plain_res, d_trace = decrypt_aes(dec_cipher_input, dec_key, is_base64=is_b64)
                
                st.subheader("Hasil Dekripsi (Plaintext Asli)")
                st.code(plain_res, language="text")
                
                st.divider()
                st.subheader("Verifikasi Pemulihan & Unpadding")
                
                v1, v2, v3 = st.columns(3)
                v1.metric("Ukuran Ciphertext (Byte)", d_trace["cipher_len"])
                v2.metric("Padding Dihapus (Byte)", d_trace["padding_removed"])
                v3.metric("Ukuran Plaintext (Byte)", d_trace["unpadded_len"])
                
                st.write("Data setelah dekripsi sebelum unpadding (Hex):")
                st.code(d_trace["decrypted_padded_hex"], language="text")
                
            except Exception as ex:
                st.error(f"Kegagalan dekripsi: {str(ex)}")
