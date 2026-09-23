# Sistem Kriptografi Terpadu

Aplikasi web untuk visualisasi dan simulasi algoritma kriptografi klasik dan modern, dibangun menggunakan Python dan Streamlit native untuk tugas mata kuliah Kriptografi (Semester 5).

---

## Modul Algoritma

1. **Vigenère Cipher (Klasik - Polialfabetik)**:
   - Enkripsi dan dekripsi periodik $(P_i \pm K_i) \pmod{26}$.
   - Visualisasi rekonstruksi pergeseran karakter demi karakter dalam bentuk tabel data.

2. **Playfair Cipher (Klasik - Bigram)**:
   - Pembentukan matriks kunci $5 \times 5$ (peleburan otomatis $J \rightarrow I$).
   - Pembagian teks menjadi pasangan huruf (digraph) dengan penyisipan huruf $X$.
   - Visualisasi matriks $5 \times 5$, daftar aturan pergeseran baris, kolom, dan persegi, serta fitur inspeksi digraph pada grid menggunakan pandas Styler.

3. **Vernam Cipher / One-Time Pad (Modern - Stream Simetris)**:
   - Enkripsi dan dekripsi $C_i = P_i \oplus K_i$ dengan kunci sepanjang pesan (dapat dibangkitkan acak otomatis).
   - Visualisasi biner plaintext, biner kunci, dan hasil XOR per byte.

4. **LFSR-based Stream Cipher (Modern - Stream Simetris)**:
   - Register geser 4/8/16 bit dengan polinomial primitif (periode maksimum $2^n - 1$) dan seed biner.
   - Visualisasi jejak clock (state, feedback XOR tap, bit output) dan XOR keystream per byte.

5. **Super Enkripsi (Kombinasi 4 Layer)**:
   - Pipa enkripsi bertingkat: $\text{Plaintext} \rightarrow \text{Playfair} \rightarrow \text{Vigenère} \rightarrow \text{LFSR} \rightarrow \text{Vernam} \rightarrow \text{Ciphertext Final (Hex)}$.
   - Pipa pembalikan (dekripsi) dengan urutan terbalik secara presisi.
   - Visualisasi proses bertahap menggunakan expander berurutan dan diagram alur standar `st.graphviz_chart`.

---

## Struktur Direktori

```
proyek1/
├── app.py                      # Halaman utama aplikasi (beranda)
├── requirements.txt            # Dependensi Python
├── .gitignore                  # Berkas pengecualian Git
├── docs/                       # Dokumentasi lengkap & persiapan presentasi
│   ├── 1_TEORI_DAN_PERHITUNGAN_MANUAL.md
│   ├── 2_BEDAH_KODE_DAN_ARSITEKTUR.md
│   ├── 3_TANYA_JAWAB_DOSEN_DAN_PENGUJIAN.md
│   └── 4_PANDUAN_PRESENTASI_DAN_SLIDE_PPT.md
├── utils/
│   ├── __init__.py
│   └── ui.py                   # Helper formatting dataframe dan pandas styler
├── ciphers/                    # Logic murni setiap algoritma kriptografi
│   ├── __init__.py
│   ├── vigenere.py
│   ├── playfair.py
│   ├── vernam.py
│   ├── lfsr.py
│   └── super_cipher.py
└── pages/                      # Multipage Streamlit
    ├── 1_Vigenere_Cipher.py
    ├── 2_Playfair_Cipher.py
    ├── 3_Vernam_Cipher.py
    ├── 4_LFSR_Stream_Cipher.py
    └── 5_Super_Enkripsi.py
```

---

## Dokumentasi & Panduan Presentasi

Folder `docs/` menyediakan panduan komprehensif untuk pengujian dan presentasi kelas:
- [1. Teori dan Perhitungan Manual](file:///d:/KULIAH/Semester%205/Kriptografi/proyek1/docs/1_TEORI_DAN_PERHITUNGAN_MANUAL.md): Konsep matematis mendalam, OTP dan perfect secrecy, LFSR dan polinomial primitif, dan simulasi hitungan manual langkah-demi-langkah.
- [2. Bedah Kode dan Arsitektur](file:///d:/KULIAH/Semester%205/Kriptografi/proyek1/docs/2_BEDAH_KODE_DAN_ARSITEKTUR.md): Penjelasan alur kode, struktur data tracer visualisasi, dan pemisahan SoC (*Separation of Concerns*).
- [3. Tanya Jawab Dosen dan Pengujian](file:///d:/KULIAH/Semester%205/Kriptografi/proyek1/docs/3_TANYA_JAWAB_DOSEN_DAN_PENGUJIAN.md): Kumpulan 19 pertanyaan kritis yang sering diajukan dosen kriptografi beserta jawaban akademis berbobot.
- [4. Panduan Slide PPT dan Live Demo](file:///d:/KULIAH/Semester%205/Kriptografi/proyek1/docs/4_PANDUAN_PRESENTASI_DAN_SLIDE_PPT.md): Strategi pembagian konten slide vs demo langsung, struktur 10 slide PPT, dan rundown waktu 20 menit.

---

## Cara Menjalankan

1. **Instal dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan aplikasi**:
   ```bash
   streamlit run app.py
   ```
