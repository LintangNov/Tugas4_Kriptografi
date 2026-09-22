import streamlit as st
import pandas as pd
from ciphers.playfair import encrypt_playfair, decrypt_playfair
from utils.ui import style_playfair_grid

st.set_page_config(
    page_title="Playfair Cipher",
    layout="wide"
)

st.header("Playfair Cipher (Klasik - Bigram)")
st.write(
    "Sandi substitusi berpasangan menggunakan matriks 5x5. Huruf J dilebur menjadi I, "
    "huruf kembar dalam satu pasangan disisipkan X, dan panjang ganjil ditambah X."
)

tab_enc, tab_dec = st.tabs(["Enkripsi", "Dekripsi"])

# ----------------- TAB ENKRIPSI -----------------
with tab_enc:
    col_in1, col_in2 = st.columns([3, 2])
    
    with col_in1:
        enc_plain = st.text_area(
            "Plaintext (Teks Asli)",
            value="TEMUI SAYA DI LABORATORIUM",
            height=120,
            key="pf_enc_plain"
        )
    
    with col_in2:
        enc_key = st.text_input(
            "Kunci (Key)",
            value="MONARCHY",
            key="pf_enc_key"
        )
        st.info("Kunci akan disusun ke matriks 5x5 tanpa duplikasi. Huruf J dilebur ke I.")

    if st.button("Proses Enkripsi", key="btn_enc_pf", use_container_width=True):
        if not enc_plain.strip():
            st.warning("Plaintext tidak boleh kosong.")
        elif not enc_key.strip():
            st.warning("Kunci tidak boleh kosong.")
        else:
            try:
                ciphertext, matrix, key_chars, steps = encrypt_playfair(enc_plain, enc_key)
                
                st.subheader("Hasil Enkripsi (Ciphertext)")
                st.code(ciphertext, language="text")
                
                st.divider()
                st.subheader("Visualisasi Matriks 5x5 & Digraph")
                
                col_mat, col_info = st.columns([1, 2])
                with col_mat:
                    st.write("**Matriks Kunci 5x5:**")
                    styled_grid = style_playfair_grid(matrix, key_chars=set(key_chars))
                    st.dataframe(styled_grid, use_container_width=True)
                    st.caption("Huruf yang digarisbawahi/tebal berasal dari kata kunci.")
                    
                with col_info:
                    st.write("**Statistik:**")
                    m1, m2 = st.columns(2)
                    m1.metric("Jumlah Digraph (Pasangan)", len(steps))
                    m2.metric("Panjang Ciphertext", len(ciphertext))
                    st.write(f"Karakter Kunci: `{', '.join(key_chars)}`")
                
                st.write("**Detail Aturan per Digraph:**")
                digraph_data = []
                for s in steps:
                    digraph_data.append({
                        "No": s["pair_idx"],
                        "Input Digraph": s["in_pair"],
                        "Posisi Input": f"({s['pos1'][0]},{s['pos1'][1]}), ({s['pos2'][0]},{s['pos2'][1]})",
                        "Aturan": s["rule"],
                        "Keterangan": s["rule_desc"],
                        "Posisi Output": f"({s['new_pos1'][0]},{s['new_pos1'][1]}), ({s['new_pos2'][0]},{s['new_pos2'][1]})",
                        "Output Digraph": s["out_pair"]
                    })
                st.dataframe(pd.DataFrame(digraph_data), use_container_width=True)
                
                with st.expander("Inspeksi Posisi Digraph pada Matriks"):
                    selected_pair_idx = st.selectbox(
                        "Pilih pasangan untuk disorot posisinya:",
                        options=range(1, len(steps) + 1),
                        format_func=lambda x: f"Digraph #{x}: {steps[x-1]['in_pair']} -> {steps[x-1]['out_pair']} ({steps[x-1]['rule']})",
                        key="sel_enc_digraph"
                    )
                    sel_step = steps[selected_pair_idx - 1]
                    hi_map = {
                        sel_step["pos1"]: "active",
                        sel_step["pos2"]: "active",
                        sel_step["new_pos1"]: "result",
                        sel_step["new_pos2"]: "result"
                    }
                    col_insp1, col_insp2 = st.columns([1, 2])
                    with col_insp1:
                        st.dataframe(style_playfair_grid(matrix, key_chars=set(key_chars), highlight_coords=hi_map), use_container_width=True)
                    with col_insp2:
                        st.write(f"**Input (Kuning):** `{sel_step['c1']}` di [{sel_step['pos1'][0]},{sel_step['pos1'][1]}] dan `{sel_step['c2']}` di [{sel_step['pos2'][0]},{sel_step['pos2'][1]}]")
                        st.write(f"**Output (Hijau):** `{sel_step['res1']}` di [{sel_step['new_pos1'][0]},{sel_step['new_pos1'][1]}] dan `{sel_step['res2']}` di [{sel_step['new_pos2'][0]},{sel_step['new_pos2'][1]}]")
                        st.info(sel_step["rule_desc"])
                        
            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")

# ----------------- TAB DEKRIPSI -----------------
with tab_dec:
    col_d1, col_d2 = st.columns([3, 2])
    
    with col_d1:
        dec_cipher = st.text_area(
            "Ciphertext (Teks Sandi)",
            value="",
            placeholder="Masukkan ciphertext Playfair...",
            height=120,
            key="pf_dec_cipher"
        )
        
    with col_d2:
        dec_key = st.text_input(
            "Kunci (Key)",
            value="MONARCHY",
            key="pf_dec_key"
        )
        st.info("Aturan dekripsi: baris sama geser kiri, kolom sama geser atas, persegi tukar kolom.")

    if st.button("Proses Dekripsi", key="btn_dec_pf", use_container_width=True):
        if not dec_cipher.strip():
            st.warning("Ciphertext tidak boleh kosong.")
        elif not dec_key.strip():
            st.warning("Kunci tidak boleh kosong.")
        else:
            try:
                dec_plain, matrix, key_chars, steps = decrypt_playfair(dec_cipher, dec_key)
                
                st.subheader("Hasil Dekripsi (Plaintext)")
                st.code(dec_plain, language="text")
                
                st.divider()
                st.subheader("Visualisasi Dekripsi Matriks 5x5")
                
                col_mat_d, col_info_d = st.columns([1, 2])
                with col_mat_d:
                    st.write("**Matriks Kunci 5x5:**")
                    st.dataframe(style_playfair_grid(matrix, key_chars=set(key_chars)), use_container_width=True)
                with col_info_d:
                    st.metric("Jumlah Digraph Diproses", len(steps))
                    
                dec_rows = []
                for s in steps:
                    dec_rows.append({
                        "No": s["pair_idx"],
                        "Cipher Digraph": s["in_pair"],
                        "Posisi Cipher": f"({s['pos1'][0]},{s['pos1'][1]}), ({s['pos2'][0]},{s['pos2'][1]})",
                        "Aturan": s["rule"],
                        "Posisi Plain": f"({s['new_pos1'][0]},{s['new_pos1'][1]}), ({s['new_pos2'][0]},{s['new_pos2'][1]})",
                        "Plain Digraph": s["out_pair"]
                    })
                st.dataframe(pd.DataFrame(dec_rows), use_container_width=True)
                
            except Exception as ex:
                st.error(f"Terjadi kesalahan: {str(ex)}")
