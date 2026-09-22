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
   Menyediakan fungsi formatting berbasis Pandas Styler untuk matriks Playfair dan matriks State AES tanpa menyuntikkan kode HTML/CSS custom yang tidak aman (*unsafe*).

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

### 2.3 Modul AES-128 (`ciphers/aes_cipher.py`)
- **Penanganan Kunci (`normalize_key_16`):**
  Mengonversi string kunci menjadi array 16 byte (`128 bit`). Jika panjang string kurang dari 16 byte, dilakukan padding karakter `#`, jika lebih dipotong 16 byte pertama.
- **Implementasi Standar Industri (PyCryptodome):**
  Fungsi enkripsi dan dekripsi utama menggunakan `Crypto.Cipher.AES` dengan mode ECB dan padding `Crypto.Util.Padding.pad(..., 16, style='pkcs7')`. Hal ini menjamin kesesuaian standar kriptografi modern FIPS PUB 197.
- **Tracer Visualisasi Blok Pertama (`trace_aes_first_block`):**
  Untuk tujuan edukatif, modul ini mengimplementasikan transformasi State Matrix langkah-demi-langkah secara manual khusus pada blok 16 byte pertama:
  - `bytes_to_state(block_bytes)`: Memetakan 16 byte ke matriks $4 \times 4$ berordo kolom (*column-major*).
  - `sub_bytes_transform(state)`: Melakukan substitusi nilai byte berdasarkan tabel lookup konstan `S_BOX` Rijndael (256 byte).
  - `shift_rows_transform(state)`: Melakukan pergeseran siklis ke kiri pada baris 1 (1 byte), baris 2 (2 byte), dan baris 3 (3 byte).
  - `mix_columns_transform(state)`: Menerapkan fungsi `xtime` untuk perkalian dalam Galois Field $GF(2^8)$ modulo polinomial tak tereduksi $x^8 + x^4 + x^3 + x + 1$.
  - `generate_round_keys(key_bytes)`: Menghasilkan 11 round key (Round 0 s/d Round 10) menggunakan rotasi kata `RotWord`, substitusi `SubWord`, dan konstanta putaran `RCON`.

### 2.4 Modul RSA (`ciphers/rsa_cipher.py`)
- **Verifikasi Prima (`is_prime`):**
  Melakukan pemeriksaan deterministik bilangan prima dengan kompleksitas waktu $O(\sqrt{n})$.
- **Extended Euclidean Algorithm (`extended_gcd`):**
  Fungsi rekursif yang menghitung nilai $x$ dan $y$ sedemikian rupa sehingga:
  $$a \cdot x + b \cdot y = \gcd(a, b)$$
- **Invers Modular (`mod_inverse`):**
  Menghitung kunci privat $d$ dari eksponen publik $e$ dan totient $\phi(n)$:
  $$d \equiv e^{-1} \pmod{\phi(n)}$$
- **Enkripsi dan Dekripsi Karakter demi Karakter:**
  - `encrypt_rsa_char_by_char`: Mengonversi karakter teks menjadi representasi ASCII desimal $M$, lalu menghitung $C = \text{pow}(M, e, n)$ menggunakan algoritma modular eksponensial bawaan Python yang efisien ($O(\log e)$).
  - `decrypt_rsa_char_by_char`: Menghitung $M = \text{pow}(C, d, n)$, lalu mengonversinya kembali menjadi karakter menggunakan `chr(M)`.

### 2.5 Modul Super Enkripsi (`ciphers/super_cipher.py`)
- Mengintegrasikan keempat modul di atas menjadi sebuah pipa komputasi berurutan:
  - **Fungsi `super_encrypt`:**
    `Plaintext -> encrypt_vigenere -> encrypt_playfair -> encrypt_aes -> encrypt_rsa_char_by_char -> Ciphertext Final`.
    Mengumpulkan kamus objek `trace` untuk setiap tahapan (1 hingga 4) yang memuat input teks, kunci yang digunakan, output parsial, dan catatan teknis.
  - **Fungsi `super_decrypt`:**
    Menerapkan pembalikan secara presisi:
    `Ciphertext Final -> decrypt_rsa_char_by_char -> decrypt_aes -> decrypt_playfair -> decrypt_vigenere -> Plaintext Asli`.

---

## 3. Modul Visualisasi dan Styler (`utils/ui.py`)

Untuk mematuhi prinsip tampilan bersih bawaan Streamlit (tanpa injeksi HTML atau CSS kustom yang rentan), modul ini memanfaatkan fitur native **Pandas Styler**:
- **`style_playfair_grid(matrix_5x5, key_chars, highlight_coords)`:**
  Membuat objek `DataFrame` $5 \times 5$, kemudian menerapkan fungsi styling sel melalui `df.style.apply`:
  - Sel pada koordinat input pasangan bigram diwarnai kuning (`#fef08a`).
  - Sel pada koordinat output transformasi diwarnai hijau muda (`#bbf7d0`).
  - Huruf yang berasal langsung dari kunci diberi gaya tebal dan garis bawah.
- **`format_aes_state_dataframe(state_4x4)`:**
  Mengonversi matriks state yang berisi nilai integer byte ($0 - 255$) menjadi DataFrame $4 \times 4$ dengan representasi string heksadesimal dua digit uppercase (`00` hingga `FF`).

---

## 4. Antarmuka Pengguna Multipage Streamlit (`pages/`)

Setiap halaman pada folder `pages/` mengikuti konvensi penamaan standar multipage Streamlit:
- `app.py`: Titik masuk utama aplikasi (beranda, ringkasan fitur, dan identitas kelompok).
- `pages/1_Vigenere_Cipher.py`: Tab Enkripsi & Dekripsi, metrik karakter, dan tabel pergeseran per karakter.
- `pages/2_Playfair_Cipher.py`: Tab Enkripsi & Dekripsi, visualisasi grid 5x5, tabel digraph, dan dropdown interaktif untuk menyorot pasangan bigram pada grid.
- `pages/3_AES_Cipher.py`: Tab Enkripsi & Dekripsi, rincian padding PKCS#7, ringkasan Round Key 0 dan 10, serta expander matriks state 4x4 Pre-Round dan Round 1.
- `pages/4_RSA_Cipher.py`: Form parameter bilangan prima $p, q$, pemilihan $e$, metrik modulus $n$, totient $\phi(n)$, kunci publik, kunci privat, serta tabel eksponensial modular per karakter.
- `pages/5_Super_Enkripsi.py`: Form input 4 kunci sekaligus, visualisasi bertingkat melalui `st.expander` untuk tiap tahap enkripsi/dekripsi, serta diagram alur pipa data menggunakan `st.graphviz_chart`.
