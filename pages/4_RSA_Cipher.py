import streamlit as st
import pandas as pd
from ciphers.rsa_cipher import is_prime, generate_rsa_keys, encrypt_rsa_char_by_char, decrypt_rsa_char_by_char, get_possible_e_values

st.set_page_config(
    page_title="RSA Cipher",
    layout="wide"
)

st.header("Rivest-Shamir-Adleman (RSA)")
st.write(
    "Algoritma kriptografi asimetris berbasis kesulitan faktorisasi prima. "
    "Kunci publik digunakan untuk enkripsi, dan kunci privat digunakan untuk dekripsi."
)

st.info(
    "Catatan Edukatif: Implementasi ini dibuat secara manual dari nol untuk tujuan demonstrasi dan "
    "pembelajaran konsep matematika (menggunakan bilangan prima kecil). "
    "Untuk penggunaan produksi nyata, diperlukan bilangan prima minimal 2048-bit dan skema padding OAEP."
)

st.subheader("1. Pembangkitan Kunci (Key Generation)")

col_k1, col_k2, col_k3 = st.columns(3)

with col_k1:
    p_val = st.number_input("Bilangan Prima p", min_value=3, max_value=5000, value=61, step=2)
    p_valid = is_prime(p_val)
    if not p_valid:
        st.caption("Status: Bukan bilangan prima!")
    else:
        st.caption("Status: Prima terverifikasi.")

with col_k2:
    q_val = st.number_input("Bilangan Prima q", min_value=3, max_value=5000, value=53, step=2)
    q_valid = is_prime(q_val)
    if not q_valid:
        st.caption("Status: Bukan bilangan prima!")
    elif q_val == p_val:
        st.caption("Status: q tidak boleh bernilai sama dengan p!")
    else:
        st.caption("Status: Prima terverifikasi.")

keys_ready = False
rsa_params = None

if p_valid and q_valid and (p_val != q_val):
    temp_phi = (p_val - 1) * (q_val - 1)
    e_candidates = get_possible_e_values(temp_phi, limit=10)
    
    with col_k3:
        sel_e = st.selectbox(
            "Eksponen Publik e (relatif prima dengan phi)",
            options=e_candidates,
            index=0
        )
        st.caption(f"Fungsi Totient Euler: phi(n) = {temp_phi}")
        
    try:
        rsa_params = generate_rsa_keys(p_val, q_val, sel_e)
        keys_ready = True
    except Exception as ex:
        st.error(f"Gagal membentuk parameter kunci: {str(ex)}")

if keys_ready and rsa_params:
    st.write("**Parameter Kunci Terbentuk:**")
    kp1, kp2, kp3, kp4 = st.columns(4)
    kp1.metric("Modulus n (p * q)", rsa_params["n"])
    kp2.metric("Euler Totient phi(n)", rsa_params["phi"])
    kp3.metric("Kunci Publik (e, n)", f"({rsa_params['e']}, {rsa_params['n']})")
    kp4.metric("Kunci Privat (d, n)", f"({rsa_params['d']}, {rsa_params['n']})")
    st.caption(f"Invers modular d dihitung dengan Extended Euclidean Algorithm: ({rsa_params['e']} * {rsa_params['d']}) mod {rsa_params['phi']} = 1")

st.divider()

st.subheader("2. Operasi Kriptografi")
tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

# ----------------- TAB ENKRIPSI -----------------
with tab_enc:
    if not keys_ready:
        st.warning("Pastikan parameter p, q, dan e sudah valid pada bagian Pembangkitan Kunci di atas.")
    else:
        col_e1, col_e2 = st.columns([3, 2])
        with col_e1:
            enc_plain = st.text_input(
                "Plaintext Masukan",
                value="KRIPTO",
                key="rsa_enc_plain"
            )
        with col_e2:
            st.info(f"Rumus: C = M^e mod n. Menggunakan e = {rsa_params['e']} dan n = {rsa_params['n']}. Syarat: M < n.")
            
        if st.button("Proses Enkripsi RSA", key="btn_enc_rsa", use_container_width=True):
            if not enc_plain.strip():
                st.warning("Plaintext tidak boleh kosong.")
            else:
                try:
                    c_ints, c_str, steps = encrypt_rsa_char_by_char(enc_plain, rsa_params["e"], rsa_params["n"])
                    
                    st.subheader("Hasil Enkripsi (Deret Integer)")
                    st.code(c_str, language="text")
                    
                    st.divider()
                    st.subheader("Visualisasi Eksponensial Modular per Karakter")
                    
                    rows = []
                    for s in steps:
                        rows.append({
                            "No": s["index"],
                            "Karakter": s["char"],
                            "Nilai ASCII (M)": s["m_val"],
                            "Operasi Modular": s["formula"],
                            "Hasil Cipher (C)": s["c_val"]
                        })
                        
                    st.dataframe(pd.DataFrame(rows), use_container_width=True)
                    
                except Exception as ex:
                    st.error(f"Gagal melakukan enkripsi: {str(ex)}")

# ----------------- TAB DEKRIPSI -----------------
with tab_dec:
    if not keys_ready:
        st.warning("Pastikan parameter p, q, dan e sudah valid pada bagian Pembangkitan Kunci di atas.")
    else:
        col_d1, col_d2 = st.columns([3, 2])
        with col_d1:
            dec_cipher_in = st.text_area(
                "Ciphertext Masukan (Deret Angka Dipisahkan Spasi)",
                value="",
                placeholder="Contoh: 1475 2891 1042 ...",
                height=100,
                key="rsa_dec_in"
            )
        with col_d2:
            st.info(f"Rumus: M = C^d mod n. Menggunakan d = {rsa_params['d']} dan n = {rsa_params['n']}.")

        if st.button("Proses Dekripsi RSA", key="btn_dec_rsa", use_container_width=True):
            if not dec_cipher_in.strip():
                st.warning("Ciphertext masukan tidak boleh kosong.")
            else:
                try:
                    plain_res, steps = decrypt_rsa_char_by_char(dec_cipher_in, rsa_params["d"], rsa_params["n"])
                    
                    st.subheader("Hasil Dekripsi (Plaintext)")
                    st.code(plain_res, language="text")
                    
                    st.divider()
                    st.subheader("Visualisasi Pemulihan Modular per Karakter")
                    
                    d_rows = []
                    for s in steps:
                        d_rows.append({
                            "No": s["index"],
                            "Cipher (C)": s["c_val"],
                            "Operasi Pemulihan": s["formula"],
                            "Nilai ASCII (M)": s["m_val"],
                            "Karakter Hasil": s["char"]
                        })
                        
                    st.dataframe(pd.DataFrame(d_rows), use_container_width=True)
                    
                except Exception as ex:
                    st.error(f"Gagal melakukan dekripsi: {str(ex)}")
