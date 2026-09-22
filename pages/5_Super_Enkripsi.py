import streamlit as st
from ciphers.super_cipher import super_encrypt, super_decrypt
from ciphers.rsa_cipher import is_prime

st.set_page_config(
    page_title="Super Enkripsi",
    layout="wide"
)

st.header("Super Enkripsi (Kombinasi 4 Algoritma)")
st.write(
    "Penggabungan 4 algoritma secara berurutan: Vigenère -> Playfair -> AES-128 -> RSA saat enkripsi, "
    "dan urutan terbalik saat dekripsi."
)

tab_enc, tab_dec, tab_diag = st.tabs([
    "Enkripsi Berlapis", 
    "Dekripsi Berlapis", 
    "Diagram Alur Pipeline"
])

# ----------------- TAB ENKRIPSI -----------------
with tab_enc:
    col_txt, col_keys = st.columns([1, 1])
    
    with col_txt:
        super_plain = st.text_area(
            "Plaintext Masukan",
            value="KRIPTOGRAFI MODERN SEMESTER LIMA",
            height=140,
            key="super_plain_in"
        )
        st.info("Setiap tahap memproses output dari tahap sebelumnya secara berurutan.")
        
    with col_keys:
        st.write("**Konfigurasi 4 Kunci:**")
        k_vig = st.text_input("Kunci Vigenère", value="SECURITY", key="s_k_vig")
        k_playfair = st.text_input("Kunci Playfair", value="CIPHERTEXT", key="s_k_pf")
        k_aes = st.text_input("Kunci AES-128 (16 Karakter)", value="KunciRahasia1234", max_chars=16, key="s_k_aes")
        
        rsa_k1, rsa_k2 = st.columns(2)
        with rsa_k1:
            p_in = st.number_input("RSA Prima p", min_value=11, max_value=5000, value=61, step=2, key="s_p")
        with rsa_k2:
            q_in = st.number_input("RSA Prima q", min_value=11, max_value=5000, value=53, step=2, key="s_q")
            
    if st.button("Proses Super Enkripsi", key="btn_run_super_enc", use_container_width=True):
        if not super_plain.strip():
            st.warning("Plaintext tidak boleh kosong.")
        elif not k_vig.strip() or not k_playfair.strip() or not k_aes.strip():
            st.warning("Seluruh kunci harus terisi.")
        elif not is_prime(p_in) or not is_prime(q_in) or p_in == q_in:
            st.warning("Nilai p dan q RSA harus berupa bilangan prima yang berbeda.")
        else:
            try:
                final_cipher, trace = super_encrypt(
                    super_plain,
                    k_vig,
                    k_playfair,
                    k_aes,
                    p_in,
                    q_in
                )
                
                st.subheader("Hasil Akhir Super Enkripsi (Ciphertext Final)")
                st.code(final_cipher, language="text")
                
                st.divider()
                st.subheader("Visualisasi Proses Bertahap (Step-by-Step)")
                
                stages = [
                    ("Tahap 1: Vigenère Cipher", trace["stage_1"]),
                    ("Tahap 2: Playfair Cipher", trace["stage_2"]),
                    ("Tahap 3: AES-128", trace["stage_3"]),
                    ("Tahap 4: RSA Asimetris (Akhir)", trace["stage_4"]),
                ]
                
                for title, s_data in stages:
                    with st.expander(title, expanded=True):
                        st.write(f"**Input:** `{s_data['input'][:80]}`{'...' if len(s_data['input']) > 80 else ''}")
                        st.write(f"**Kunci:** `{s_data['key']}`")
                        st.write("**Output:**")
                        st.code(s_data['output'], language="text")
                        st.caption(s_data['details'])
                        
            except Exception as ex:
                st.error(f"Gagal melakukan Super Enkripsi: {str(ex)}")

# ----------------- TAB DEKRIPSI -----------------
with tab_dec:
    col_d_txt, col_d_keys = st.columns([1, 1])
    
    with col_d_txt:
        super_dec_in = st.text_area(
            "Ciphertext Masukan (Deret Angka RSA)",
            value="",
            placeholder="Tempelkan ciphertext hasil enkripsi di sini...",
            height=140,
            key="super_dec_in"
        )
        st.info("Urutan dekripsi adalah kebalikan dari enkripsi: RSA -> AES-128 -> Playfair -> Vigenère.")
        
    with col_d_keys:
        st.write("**Konfigurasi 4 Kunci Dekripsi:**")
        d_k_vig = st.text_input("Kunci Vigenère", value="SECURITY", key="s_d_vig")
        d_k_playfair = st.text_input("Kunci Playfair", value="CIPHERTEXT", key="s_d_pf")
        d_k_aes = st.text_input("Kunci AES-128", value="KunciRahasia1234", max_chars=16, key="s_d_aes")
        
        d_rsa1, d_rsa2 = st.columns(2)
        with d_rsa1:
            d_p = st.number_input("RSA Prima p", min_value=11, max_value=5000, value=61, step=2, key="s_d_p")
        with d_rsa2:
            d_q = st.number_input("RSA Prima q", min_value=11, max_value=5000, value=53, step=2, key="s_d_q")

    if st.button("Proses Super Dekripsi", key="btn_run_super_dec", use_container_width=True):
        if not super_dec_in.strip():
            st.warning("Ciphertext masukan tidak boleh kosong.")
        elif not d_k_vig.strip() or not d_k_playfair.strip() or not d_k_aes.strip():
            st.warning("Seluruh kunci harus terisi lengkap.")
        elif not is_prime(d_p) or not is_prime(d_q) or d_p == d_q:
            st.warning("Nilai p dan q RSA harus berupa bilangan prima yang berbeda.")
        else:
            try:
                rec_plain, d_trace = super_decrypt(
                    super_dec_in,
                    d_k_vig,
                    d_k_playfair,
                    d_k_aes,
                    d_p,
                    d_q
                )
                
                st.subheader("Hasil Akhir Super Dekripsi (Plaintext Asli)")
                st.code(rec_plain, language="text")
                
                st.divider()
                st.subheader("Visualisasi Pembalikan Bertahap")
                
                d_stages = [
                    ("Tahap 1: Dekripsi RSA (Menghasilkan Base64)", d_trace["stage_1"]),
                    ("Tahap 2: Dekripsi AES-128 (Menghasilkan Teks Playfair)", d_trace["stage_2"]),
                    ("Tahap 3: Dekripsi Playfair (Menghasilkan Teks Vigenère)", d_trace["stage_3"]),
                    ("Tahap 4: Dekripsi Vigenère (Menghasilkan Plaintext Asli)", d_trace["stage_4"]),
                ]
                
                for title, s_data in d_stages:
                    with st.expander(title, expanded=True):
                        st.write(f"**Input:** `{s_data['input'][:80]}`{'...' if len(s_data['input']) > 80 else ''}")
                        st.write(f"**Kunci:** `{s_data['key']}`")
                        st.write("**Output Pemulihan:**")
                        st.code(s_data['output'], language="text")
                        st.caption(s_data['details'])

            except Exception as ex:
                st.error(f"Gagal melakukan Super Dekripsi: {str(ex)}")

# ----------------- TAB DIAGRAM ALUR -----------------
with tab_diag:
    st.subheader("Diagram Alur Pipeline Super Enkripsi")
    st.write("Diagram alur proses enkripsi dan dekripsi berlapis:")
    
    pipeline_dot = """
    digraph SuperCrypto {
        rankdir=LR;
        node [shape=box];

        plain [label="Plaintext"];
        vig   [label="1. Vigenere"];
        pf    [label="2. Playfair"];
        aes   [label="3. AES-128"];
        rsa   [label="4. RSA"];
        final [label="Ciphertext Final"];

        plain -> vig -> pf -> aes -> rsa -> final;
    }
    """
    st.graphviz_chart(pipeline_dot, use_container_width=True)
    
    st.write("**Keterangan Alur:**")
    st.write("1. **Vigenère Cipher**: Mengaburkan frekuensi huruf alfabet melalui pergeseran periodik.")
    st.write("2. **Playfair Cipher**: Mengenkripsi pasangan huruf (digraph) dengan aturan matriks 5x5.")
    st.write("3. **AES-128**: Mengenkripsi blok data dengan jaringan substitusi-permutasi (SPN) dan padding PKCS#7.")
    st.write("4. **RSA**: Melindungi data dengan enkripsi kunci publik menggunakan modular exponentiation.")
    st.write("5. **Dekripsi**: Menjalankan invers dari setiap algoritma dalam urutan terbalik (RSA -> AES -> Playfair -> Vigenère).")
