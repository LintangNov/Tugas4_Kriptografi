# Panduan Bedah Kode dan Arsitektur Aplikasi

Dokumen ini ditujukan untuk membedah struktur internal program secara teknis. Tujuannya adalah memastikan setiap anggota tim memahami implementasi fungsi, aliran data (*data flow*), serta alasan teknis di balik pemilihan struktur kode.

---

## 1. Desain Arsitektur Perangkat Lunak

Aplikasi ini mengadopsi pola pemisahan tanggung jawab (*Separation of Concerns* / SoC):

```
                     +---------------------------------------+
                     |         Streamlit Web Interface       |
                     |  (app.py & pages/*.py)                |
                     +---------------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     |         Visual & Styler Helpers       |
                     |  (utils/ui.py)                        |
                     +---------------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     |         Core Cryptographic Engine     |
                     |  (ciphers/*.py)                       |
                     +---------------------------------------+
```

### Prinsip Utama:
1. **Modul Kriptografi Murni (`ciphers/`):**
   Tidak ada kode Streamlit sama sekali di dalam modul ini. Setiap modul murni menerima parameter Python primitif (`str`, `int`, `bytes`) dan mengembalikan *tuple* berisikan teks hasil serta struktur data langkah-langkah penelusuran (*trace data*). Hal ini membuat fungsi algoritma dapat diuji secara independen melalui *unit testing* atau skrip CLI.
2. **Lapisan Presentasi (`pages/` & `app.py`):**
   Hanya bertanggung jawab menangani interaksi pengguna, validasi input antarmuka, rendering komponen native Streamlit (`st.header`, `st.tabs`, `st.expander`), dan menampilkan tabel visualisasi.
3. **Formatters (`utils/ui.py`):**
   Menyediakan fungsi formatting berbasis Pandas Styler untuk matriks Playfair tanpa menyuntikkan kode HTML/CSS custom yang tidak aman (*unsafe*).

---

## 2. Bedah Detail Modul Algoritma (`ciphers/`)

### 2.1 Modul Vigenère (`ciphers/vigenere.py`)
- **Fungsi `clean_key(key)`:**
  Menyaring karakter non-alfabet dari string kunci dan mengonversinya ke huruf kapital.
- **Fungsi `encrypt_vigenere(plaintext, key)` & `decrypt_vigenere(ciphertext, key)`:**
  - Menghitung panjang kunci efektif.
  - Melakukan perulangan karakter per karakter.
  - Untuk karakter alfabet:
    - Menghitung nilai numerik $P = \text{ord}(c) - \text{ord}('A')$.
    - Menghitung nilai pergeseran kunci $K$ dengan modulo indeks kunci `key_idx % key_len`.
    - Menerapkan pergeseran modular: `(P + K) % 26` atau `(C - K + 26) % 26`.
    - Mempertahankan status kapital/huruf kecil (*case sensitivity*).
    - Menambahkan kamus objek langkah ke dalam daftar `steps` untuk keperluan visualisasi tabel.
  - Untuk karakter non-alfabet:
    - Karakter dilewatkan apa adanya tanpa memajukan pointer indeks kunci (`key_idx`).

### 2.2 Modul Playfair (`ciphers/playfair.py`)
- **Fungsi `prepare_playfair_key(key)`:**
  - Mengonversi teks kunci ke huruf kapital.
  - Mengganti huruf `J` menjadi `I`.
  - Menggunakan himpunan `seen = set()` untuk memastikan setiap huruf hanya muncul tepat satu kali.
  - Menyusun sisa alfabet (tanpa `J`) ke dalam matriks $5 \times 5$.
  - Mengembalikan representasi list dua dimensi `matrix[5][5]` dan daftar huruf kunci asli `key_chars`.
- **Fungsi `prepare_text_for_playfair(text)`:**
  - Menyaring teks hanya untuk karakter alfabet dan melebur `J -> I`.
  - Memecah teks menjadi pasangan (*digraph*).
  - Jika sepasang huruf bernilai identik (misal: `AA`), disisipkan huruf pemisah `X` (atau `Z` jika huruf kembar tersebut adalah `X`), lalu pointer maju 1 karakter.
  - Jika tersisa 1 karakter di akhir teks (jumlah ganjil), ditambahkan huruf pengisi `X` (atau `Z`).
- **Fungsi `encrypt_playfair(...)` & `decrypt_playfair(...)`:**
  - Untuk setiap pasangan bigram $(c_1, c_2)$, dicari koordinat baris dan kolom `(r1, col1)` serta `(r2, col2)`.
  - Mengevaluasi 3 kondisi:
    - `r1 == r2` (Baris Sama): geser kolom secara sirkular $(\pm 1) \pmod 5$.
    - `col1 == col2` (Kolom Sama): geser baris secara sirkular $(\pm 1) \pmod 5$.
    - `r1 != r2 and col1 != col2` (Persegi Panjang): tukar kolom $(r_1, c_2)$ dan $(r_2, c_1)$.
  - Menyimpan informasi aturan dan koordinat untuk fitur penyorotan sel matriks pada antarmuka pengguna.

### 2.3 Modul Vernam (`ciphers/vernam.py`)
- **Pembangkit Kunci (`generate_vernam_key`):**
  Membangkitkan kunci acak dari huruf dan angka menggunakan modul `secrets` (CSPRNG), dengan panjang sama dengan pesan.
- **Inti Operasi (`vernam_xor_bytes(data, key)`):**
  Memvalidasi bahwa panjang kunci sama persis dengan panjang data (aturan OTP), lalu meng-XOR tiap byte. Fungsi ini juga mengembalikan *trace* per byte (karakter, ASCII, biner P, biner K, hasil XOR, hex). Karena XOR adalah invers dirinya sendiri, fungsi yang sama dipakai untuk enkripsi dan dekripsi.
- **Pembungkus Teks (`encrypt_vernam`, `decrypt_vernam`):**
  Mengonversi teks UTF-8 ke byte, memanggil `vernam_xor_bytes`, dan mengembalikan/menerima ciphertext dalam heksadesimal.

### 2.4 Modul LFSR Stream Cipher (`ciphers/lfsr.py`)
- **Konfigurasi (`LFSR_TAPS`):**
  Kamus tap polinomial primitif untuk register 4, 8, dan 16 bit ($x^4+x^3+1$, $x^8+x^6+x^5+x^4+1$, $x^{16}+x^{14}+x^{13}+x^{11}+1$) sehingga periode selalu maksimum $2^n - 1$.
- **Validasi Seed (`parse_seed`):**
  Memastikan seed berupa string biner tepat $n$ digit dan tidak semua nol.
- **Satu Clock (`lfsr_clock`):**
  Output = LSB; feedback = XOR bit pada posisi tap (posisi tap $t$ dipetakan ke indeks bit $n - t$); register digeser kanan dan feedback dimasukkan di MSB.
- **Pembangkit Keystream (`lfsr_keystream_bytes`):**
  Menjalankan 8 clock per byte dan menyusun bit output (bit pertama = MSB) menjadi byte keystream.
- **Enkripsi/Dekripsi Simetris (`lfsr_crypt_bytes`):**
  Meng-XOR data dengan keystream, mengembalikan byte hasil, *trace* per byte, dan *trace* clock (24 clock pertama) untuk visualisasi state register.
- **Pembungkus Teks (`encrypt_lfsr`, `decrypt_lfsr`):** Menerima teks/hex dan mengembalikan hex/teks.

### 2.5 Modul Super Enkripsi (`ciphers/super_cipher.py`)
- Mengintegrasikan keempat modul menjadi pipa komputasi berurutan:
  - **Fungsi `super_encrypt`:**
    `Plaintext -> encrypt_playfair -> encrypt_vigenere -> lfsr_crypt_bytes -> vernam_xor_bytes -> Ciphertext Final (Hex)`.
    Antara LFSR dan Vernam data diteruskan sebagai byte mentah (bukan teks) agar tidak ada penggandaan panjang. Jika kunci Vernam tidak diberikan, dibangkitkan otomatis sepanjang keluaran LFSR dan dikembalikan pada `trace["vernam_key"]`. Mengumpulkan kamus objek `trace` untuk setiap tahapan (1 hingga 4).
  - **Fungsi `super_decrypt`:**
    Menerapkan pembalikan secara presisi:
    `Ciphertext (Hex) -> vernam_xor_bytes -> lfsr_crypt_bytes -> decrypt_vigenere -> decrypt_playfair -> Plaintext Asli`.
- **Alasan Playfair di depan:** Playfair menggabungkan $J$ dan $I$; bila dijalankan setelah Vigenère, huruf $J$ pada ciphertext Vigenère akan rusak menjadi $I$. Dengan Playfair pertama, seluruh tahap sesudahnya invertibel penuh.

---

## 3. Modul Visualisasi dan Styler (`utils/ui.py`)

Untuk mematuhi prinsip tampilan bersih bawaan Streamlit (tanpa injeksi HTML atau CSS kustom yang rentan), modul ini memanfaatkan fitur native **Pandas Styler**:
- **`style_playfair_grid(matrix_5x5, key_chars, highlight_coords)`:**
  Membuat objek `DataFrame` $5 \times 5$, kemudian menerapkan fungsi styling sel melalui `df.style.apply`:
  - Sel pada koordinat input pasangan bigram diwarnai kuning (`#fef08a`).
  - Sel pada koordinat output transformasi diwarnai hijau muda (`#bbf7d0`).
  - Huruf yang berasal langsung dari kunci diberi gaya tebal dan garis bawah.

Halaman Vernam dan LFSR menampilkan visualisasi langsung dengan `st.dataframe` dari data *trace* sehingga tidak memerlukan helper tambahan.

---

## 4. Antarmuka Pengguna Multipage Streamlit (`pages/`)

Setiap halaman pada folder `pages/` mengikuti konvensi penamaan standar multipage Streamlit:
- `app.py`: Titik masuk utama aplikasi (beranda, ringkasan fitur, dan identitas kelompok).
- `pages/1_Vigenere_Cipher.py`: Tab Enkripsi & Dekripsi, metrik karakter, dan tabel pergeseran per karakter.
- `pages/2_Playfair_Cipher.py`: Tab Enkripsi & Dekripsi, visualisasi grid 5x5, tabel digraph, dan dropdown interaktif untuk menyorot pasangan bigram pada grid.
- `pages/3_Vernam_Cipher.py`: Tab Enkripsi & Dekripsi, opsi kunci acak otomatis, tabel XOR per byte (biner P, biner K, hasil XOR, hex).
- `pages/4_LFSR_Stream_Cipher.py`: Pemilihan panjang register (4/8/16 bit), input seed biner, tabel jejak clock (state, feedback, output bit), dan tabel XOR keystream per byte.
- `pages/5_Super_Enkripsi.py`: Form input kunci Playfair, Vigenère, LFSR (register + seed), dan Vernam, visualisasi bertingkat melalui `st.expander` untuk tiap tahap enkripsi/dekripsi, serta diagram alur pipa data menggunakan `st.graphviz_chart`.
