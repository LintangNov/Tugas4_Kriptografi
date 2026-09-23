import streamlit as st
from ciphers.super_cipher import super_encrypt, super_decrypt
from ciphers.lfsr import LFSR_TAPS, polynomial_str

st.set_page_config(
    page_title="Super Enkripsi",
    layout="wide"
)

DEFAULT_SEEDS = {4: "1001", 8: "10110001", 16: "1010110011100001"}

st.header("Super Enkripsi (Kombinasi 4 Algoritma)")
st.write(
    "Penggabungan 4 algoritma secara berurutan: Playfair -> Vigenère -> LFSR Stream Cipher -> Vernam (OTP) saat enkripsi, "
    "dan urutan terbalik saat dekripsi."
)

tab_enc, tab_dec, tab_diag = st.tabs([
    "Enkripsi Berlapis",
    "Dekripsi Berlapis",
    "Diagram Alur Pipeline"
])


def show_stages(stages, out_label):
    for title, s_data in stages:
        with st.expander(title, expanded=True):
            st.write(f"**Input:** `{s_data['input'][:80]}`{'...' if len(s_data['input']) > 80 else ''}")
            st.write(f"**Kunci:** `{s_data['key']}`")
            st.write(out_label)
            st.code(s_data['output'], language="text")
            st.caption(s_data['details'])


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
        st.write("**Konfigurasi Kunci:**")
        k_vig = st.text_input("Kunci Vigenère", value="SECURITY", key="s_k_vig")
        k_playfair = st.text_input("Kunci Playfair", value="CIPHERTEXT", key="s_k_pf")

        l1, l2 = st.columns(2)
        with l1:
            lfsr_n = st.selectbox("Register LFSR (bit)", list(LFSR_TAPS.keys()), index=2, key="s_lfsr_n")
        with l2:
            lfsr_seed = st.text_input("Seed LFSR (biner)", value=DEFAULT_SEEDS[lfsr_n], key=f"s_lfsr_seed_{lfsr_n}")
        st.caption(f"Polinomial LFSR: {polynomial_str(lfsr_n)}")

        auto_key = st.checkbox("Bangkitkan kunci Vernam (OTP) acak otomatis", value=True, key="s_vn_auto")
        vn_key = st.text_input(
            "Kunci Vernam (panjang = panjang output LFSR)",
            value="",
            disabled=auto_key,
            key="s_vn_key"
        )

    if st.button("Proses Super Enkripsi", key="btn_run_super_enc", use_container_width=True):
        if not super_plain.strip():
            st.warning("Plaintext tidak boleh kosong.")
        elif not k_vig.strip() or not k_playfair.strip():
            st.warning("Kunci Vigenère dan Playfair harus terisi.")
        elif not auto_key and not vn_key:
            st.warning("Kunci Vernam harus diisi atau aktifkan pembangkitan otomatis.")
        else:
            try:
                final_cipher, trace = super_encrypt(
                    super_plain,
                    k_vig,
                    k_playfair,
                    lfsr_seed,
                    lfsr_n,
                    None if auto_key else vn_key
                )

                st.subheader("Hasil Akhir Super Enkripsi (Ciphertext Final, Heksadesimal)")
                st.code(final_cipher, language="text")
                st.write("**Kunci Vernam (OTP) — wajib disimpan untuk dekripsi:**")
                st.code(trace["vernam_key"], language="text")

                st.divider()
                st.subheader("Visualisasi Proses Bertahap (Step-by-Step)")

                show_stages([
                    ("Tahap 1: Playfair Cipher", trace["stage_1"]),
                    ("Tahap 2: Vigenère Cipher", trace["stage_2"]),
                    ("Tahap 3: LFSR Stream Cipher (output heksadesimal)", trace["stage_3"]),
                    ("Tahap 4: Vernam Cipher / OTP (Akhir)", trace["stage_4"]),
                ], "**Output:**")

            except Exception as ex:
                st.error(f"Gagal melakukan Super Enkripsi: {str(ex)}")

# ----------------- TAB DEKRIPSI -----------------
with tab_dec:
    col_d_txt, col_d_keys = st.columns([1, 1])

    with col_d_txt:
        super_dec_in = st.text_area(
            "Ciphertext Masukan (Heksadesimal)",
            value="",
            placeholder="Tempelkan ciphertext hasil enkripsi di sini...",
            height=140,
            key="super_dec_in"
        )
        st.info("Urutan dekripsi adalah kebalikan dari enkripsi: Vernam -> LFSR -> Vigenère -> Playfair.")

    with col_d_keys:
        st.write("**Konfigurasi Kunci Dekripsi:**")
        d_k_vig = st.text_input("Kunci Vigenère", value="SECURITY", key="s_d_vig")
        d_k_playfair = st.text_input("Kunci Playfair", value="CIPHERTEXT", key="s_d_pf")

        dl1, dl2 = st.columns(2)
        with dl1:
            d_lfsr_n = st.selectbox("Register LFSR (bit)", list(LFSR_TAPS.keys()), index=2, key="s_d_lfsr_n")
        with dl2:
            d_lfsr_seed = st.text_input("Seed LFSR (biner)", value=DEFAULT_SEEDS[d_lfsr_n], key=f"s_d_lfsr_seed_{d_lfsr_n}")

        d_vn_key = st.text_input("Kunci Vernam (OTP)", value="", key="s_d_vn_key")

    if st.button("Proses Super Dekripsi", key="btn_run_super_dec", use_container_width=True):
        if not super_dec_in.strip():
            st.warning("Ciphertext masukan tidak boleh kosong.")
        elif not d_k_vig.strip() or not d_k_playfair.strip() or not d_vn_key:
            st.warning("Seluruh kunci (termasuk kunci Vernam) harus terisi lengkap.")
        else:
            try:
                rec_plain, d_trace = super_decrypt(
                    super_dec_in,
                    d_k_vig,
                    d_k_playfair,
                    d_lfsr_seed,
                    d_lfsr_n,
                    d_vn_key
                )

                st.subheader("Hasil Akhir Super Dekripsi (Plaintext Asli)")
                st.code(rec_plain, language="text")

                st.divider()
                st.subheader("Visualisasi Pembalikan Bertahap")

                show_stages([
                    ("Tahap 1: Dekripsi Vernam (Menghasilkan Byte LFSR)", d_trace["stage_1"]),
                    ("Tahap 2: Dekripsi LFSR (Menghasilkan Teks Vigenère)", d_trace["stage_2"]),
                    ("Tahap 3: Dekripsi Vigenère (Menghasilkan Teks Playfair)", d_trace["stage_3"]),
                    ("Tahap 4: Dekripsi Playfair (Menghasilkan Plaintext Asli)", d_trace["stage_4"]),
                ], "**Output Pemulihan:**")

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
        pf    [label="1. Playfair"];
        vig   [label="2. Vigenere"];
        lfsr  [label="3. LFSR Stream"];
        vn    [label="4. Vernam (OTP)"];
        final [label="Ciphertext Final (Hex)"];

        plain -> pf -> vig -> lfsr -> vn -> final;
    }
    """
    st.graphviz_chart(pipeline_dot, use_container_width=True)

    st.write("**Keterangan Alur:**")
    st.write("1. **Playfair Cipher**: Mengenkripsi pasangan huruf (digraph) dengan aturan matriks 5x5.")
    st.write("2. **Vigenère Cipher**: Mengaburkan frekuensi huruf alfabet melalui pergeseran periodik.")
    st.write("3. **LFSR Stream Cipher**: Membangkitkan keystream dari register geser berumpan balik linear, lalu XOR dengan data.")
    st.write("4. **Vernam Cipher (OTP)**: XOR byte hasil LFSR dengan kunci acak sepanjang data yang hanya dipakai sekali.")
    st.write("5. **Dekripsi**: Menjalankan invers dari setiap algoritma dalam urutan terbalik (Vernam -> LFSR -> Vigenère -> Playfair).")
