import streamlit as st

st.set_page_config(
    page_title="Sistem Kriptografi Terpadu",
    layout="wide"
)

st.title("Sistem Kriptografi Terpadu: Klasik, Modern, dan Super Enkripsi")
st.write(
    """
    Aplikasi web ini dibangun untuk tugas mata kuliah Kriptografi (Semester 5). 
    Platform ini menyediakan visualisasi proses enkripsi dan dekripsi langkah-demi-langkah 
    secara transparan, baik untuk algoritma klasik (Vigenère dan Playfair), algoritma modern (AES dan RSA), 
    maupun kombinasi berurutan (Super Enkripsi).
    """
)

st.divider()

st.subheader("Menu Algoritma")
st.write("Silakan pilih salah satu menu di sidebar sebelah kiri untuk memulai simulasi:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. Vigenère Cipher (Klasik - Polialfabetik)**")
    st.write(
        "Sandi substitusi polialfabetik berbasis pergeseran periodik dengan kata kunci. "
        "Menampilkan tabel pergeseran indeks, rumus modulo 26, dan karakter hasil."
    )
    
    st.markdown("**3. Advanced Encryption Standard / AES (Modern - Blok Simetris)**")
    st.write(
        "Standar enkripsi blok simetris 128-bit (Rijndael). "
        "Menampilkan proses PKCS#7 padding, key expansion, serta visualisasi state matrix 4x4 pada setiap tahapan round."
    )

with col2:
    st.markdown("**2. Playfair Cipher (Klasik - Bigram)**")
    st.write(
        "Sandi substitusi bigram berbasis matriks kunci 5x5. "
        "Menampilkan grid matriks, pemecahan huruf kembar dan ganjil, serta aturan pergeseran baris, kolom, dan persegi."
    )

    st.markdown("**4. Rivest-Shamir-Adleman / RSA (Modern - Asimetris Kunci Publik)**")
    st.write(
        "Kriptografi kunci publik manual menggunakan bilangan prima untuk demonstrasi edukatif. "
        "Menampilkan pembentukan parameter n, totient Euler, pemilihan e, pencarian d (Extended Euclidean), dan eksponensial modular."
    )

st.markdown("**5. Super Enkripsi (Kombinasi 4 Layer)**")
st.write(
    "Penggabungan 4 algoritma secara berurutan: Vigenère -> Playfair -> AES-128 -> RSA saat enkripsi, "
    "dan urutan terbalik saat dekripsi, dilengkapi visualisasi tahapan dan diagram alur."
)

st.divider()

st.subheader("Identitas Kelompok")
col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    st.write("**Anggota 1:**")
    st.write("Nama: [Nama Mahasiswa 1]")
    st.write("NIM: [NIM Mahasiswa 1]")

with col_t2:
    st.write("**Anggota 2:**")
    st.write("Nama: [Nama Mahasiswa 2]")
    st.write("NIM: [NIM Mahasiswa 2]")

with col_t3:
    st.write("**Anggota 3:**")
    st.write("Nama: [Nama Mahasiswa 3]")
    st.write("NIM: [NIM Mahasiswa 3]")

with st.sidebar:
    st.write("### Kriptografi - Proyek 1")
    st.caption("Pilih modul di atas untuk menjalankan pengujian.")
