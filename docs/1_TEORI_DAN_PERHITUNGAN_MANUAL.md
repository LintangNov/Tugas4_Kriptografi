# Panduan Teori Dasar dan Perhitungan Manual Algoritma Kriptografi

Dokumen ini disusun sebagai referensi akademis komprehensif bagi tim pengembang untuk memahami prinsip teoritis, formulasi matematika, dan simulasi perhitungan manual dari seluruh algoritma yang diimplementasikan dalam aplikasi: Vigenère Cipher, Playfair Cipher, Vernam Cipher (One-Time Pad), LFSR-based Stream Cipher, serta Super Enkripsi.

---

## 1. Vigenère Cipher (Klasik - Polialfabetik)

### 1.1 Teori Dasar
Vigenère Cipher adalah metode penyandian teks alfabet menggunakan variasi sandi Caesar berbasis kata kunci (*polyalphabetic substitution cipher*). Berbeda dengan sandi monoalfabetik (seperti Caesar biasa) di mana satu huruf plaintext selalu dipetakan ke huruf ciphertext yang sama, Vigenère menggunakan pergeseran yang berubah-ubah secara periodik tergantung huruf kunci yang bersesuaian. Karakteristik ini membuat Vigenère jauh lebih tahan terhadap analisis frekuensi huruf tunggal sederhana.

Alfabet standar A-Z dipetakan ke dalam bilangan bulat $0$ sampai $25$:
`A=0, B=1, C=2, ..., Z=25`.

### 1.2 Formulasi Matematika
- **Enkripsi:**
  $$C_i = (P_i + K_{i \pmod m}) \pmod{26}$$
  dengan:
  - $P_i$: nilai numerik karakter plaintext ke-$i$.
  - $K_{i \pmod m}$: nilai numerik karakter kunci ke-$(i \pmod m)$, dengan $m$ adalah panjang kunci.
  - $C_i$: nilai numerik karakter ciphertext ke-$i$.

- **Dekripsi:**
  $$P_i = (C_i - K_{i \pmod m} + 26) \pmod{26}$$
  Penambahan nilai $26$ bertujuan menghindari hasil negatif pada operasi modulo dalam aritmatika komputer.

### 1.3 Contoh Perhitungan Manual
- **Plaintext:** `KRIPTO`
- **Kunci:** `KUNCI` (panjang $m = 5$)

Langkah perataan kunci secara periodik:
- Karakter 1: P = `K` (10), K = `K` (10)
  $$C_1 = (10 + 10) \pmod{26} = 20 \rightarrow \text{U}$$
- Karakter 2: P = `R` (17), K = `U` (20)
  $$C_2 = (17 + 20) \pmod{26} = 37 \pmod{26} = 11 \rightarrow \text{L}$$
- Karakter 3: P = `I` (8), K = `N` (13)
  $$C_3 = (8 + 13) \pmod{26} = 21 \rightarrow \text{V}$$
- Karakter 4: P = `P` (15), K = `C` (2)
  $$C_4 = (15 + 2) \pmod{26} = 17 \rightarrow \text{R}$$
- Karakter 5: P = `T` (19), K = `I` (8)
  $$C_5 = (19 + 8) \pmod{26} = 27 \pmod{26} = 1 \rightarrow \text{B}$$
- Karakter 6: P = `O` (14), K = `K` (10) [Kunci kembali berulang ke indeks 0]
  $$C_6 = (14 + 10) \pmod{26} = 24 \rightarrow \text{Y}$$

Hasil Ciphertext: `ULVRBY`.

Proses Dekripsi untuk Karakter 2:
$$P_2 = (11 - 20 + 26) \pmod{26} = 17 \rightarrow \text{R (Plaintext awal pulih)}$$

---

## 2. Playfair Cipher (Klasik - Bigram)

### 2.1 Teori Dasar
Playfair Cipher diciptakan oleh Charles Wheatstone pada tahun 1854 dan dipopulerkan oleh Lord Playfair. Algoritma ini menyandikan pasangan huruf (*bigram* atau *digraph*), bukan huruf tunggal. Hal ini menggagalkan analisis frekuensi huruf tunggal karena terdapat $25 \times 25 = 625$ kemungkinan kombinasi pasangan huruf.

Aturan pembentukan matriks:
1. Matriks berukuran $5 \times 5$ (total 25 sel).
2. Alfabet berjumlah 26 huruf, sehingga huruf `I` dan `J` digabungkan dalam satu sel (dalam implementasi sistem ini, `J` dikonversi menjadi `I`).
3. Kunci ditulis di awal matriks dengan membuang huruf duplikat. Sisa sel kosong diisi huruf alfabet yang belum digunakan secara berurutan.

Aturan pemrosesan teks (digraph preparation):
1. Jika terdapat dua huruf kembar dalam satu pasangan (misal: `EE`), sisipkan huruf pengisi `X` di antaranya sehingga menjadi `EX` dan `E...`.
2. Jika jumlah huruf ganjil di akhir teks, tambahkan huruf pengisi `X` (atau `Z` jika huruf terakhir adalah `X`).

### 2.2 Aturan Transformasi Geometri Matriks
Untuk setiap pasangan huruf $(r_1, c_1)$ dan $(r_2, c_2)$:
1. **Baris Sama ($r_1 = r_2$):**
   - Enkripsi: Geser 1 kolom ke kanan secara sirkular: $c' = (c + 1) \pmod 5$.
   - Dekripsi: Geser 1 kolom ke kiri secara sirkular: $c' = (c - 1 + 5) \pmod 5$.
2. **Kolom Sama ($c_1 = c_2$):**
   - Enkripsi: Geser 1 baris ke bawah secara sirkular: $r' = (r + 1) \pmod 5$.
   - Dekripsi: Geser 1 baris ke atas secara sirkular: $r' = (r - 1 + 5) \pmod 5$.
3. **Persegi Panjang / Sudut Berseberangan ($r_1 \ne r_2$ dan $c_1 \ne c_2$):**
   - Huruf pertama digantikan oleh huruf pada baris yang sama di kolom huruf kedua: $(r_1, c_2)$.
   - Huruf kedua digantikan oleh huruf pada baris yang sama di kolom huruf pertama: $(r_2, c_1)$.
   - Aturan ini simetris antara enkripsi dan dekripsi.

### 2.3 Contoh Perhitungan Manual
- **Kunci:** `MONARCHY`
- **Plaintext:** `LABORATORIUM`

Penyusunan Matriks 5x5:
```
M  O  N  A  R
C  H  Y  B  D
E  F  G  I  K
L  P  Q  S  T
U  V  W  X  Z
```

Pembagian Digraph:
`LA - BO - RA - TO - RI - UM` (semua pasangan valid, jumlah genap: 12 huruf = 6 pasang).

Simulasi Transformasi Pasangan:
1. `LA`:
   - `L` berada di baris 3, kolom 0.
   - `A` berada di baris 0, kolom 3.
   - Aturan: Persegi Panjang.
   - Hasil: `L` -> matriks[3][3] = `S`, `A` -> matriks[0][0] = `M` -> **`SM`**.
2. `BO`:
   - `B` berada di baris 1, kolom 3.
   - `O` berada di baris 0, kolom 1.
   - Aturan: Persegi Panjang.
   - Hasil: `B` -> matriks[1][1] = `H`, `O` -> matriks[0][3] = `A` -> **`HA`**.
3. `RA`:
   - `R` berada di baris 0, kolom 4.
   - `A` berada di baris 0, kolom 3.
   - Aturan: Baris Sama (baris 0).
   - Hasil: `R` -> geser kanan -> `M` (kolom 0 sirkular), `A` -> geser kanan -> `R` -> **`MR`**.

---

## 3. Vernam Cipher / One-Time Pad (Modern - Stream Simetris)

### 3.1 Teori Dasar
Vernam Cipher (Gilbert Vernam, 1917) adalah sandi aliran (*stream cipher*) yang meng-XOR setiap bit plaintext dengan bit kunci pada posisi yang sama. Jika kunci memenuhi tiga syarat berikut, sandi ini disebut **One-Time Pad (OTP)** dan terbukti aman secara teoretis (*perfect secrecy*, Shannon 1949):
1. Kunci **benar-benar acak**.
2. Panjang kunci **sama persis** dengan panjang pesan.
3. Kunci **hanya dipakai satu kali** (tidak boleh digunakan ulang).

Pada perfect secrecy, ciphertext tidak memberikan informasi apa pun tentang plaintext: setiap plaintext dengan panjang yang sama sama-sama mungkin menghasilkan ciphertext tersebut, tergantung kunci yang dipakai.

### 3.2 Formulasi Matematika
Operasi dilakukan per bit (atau per byte) dengan XOR ($\oplus$):
- **Enkripsi:** $C_i = P_i \oplus K_i$
- **Dekripsi:** $P_i = C_i \oplus K_i$

Dekripsi memakai operasi yang sama karena XOR adalah invers dirinya sendiri:
$$(P \oplus K) \oplus K = P \oplus (K \oplus K) = P \oplus 0 = P$$

Tabel kebenaran XOR: $0 \oplus 0 = 0$, $0 \oplus 1 = 1$, $1 \oplus 0 = 1$, $1 \oplus 1 = 0$.

### 3.3 Contoh Perhitungan Manual
- **Plaintext:** `HALO`
- **Kunci OTP:** `Xk9#` (panjang 4 = panjang pesan)

| Char P | ASCII | Biner P | Char K | Biner K | P $\oplus$ K | Hex C |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `H` | 72 | 01001000 | `X` | 01011000 | 00010000 | `10` |
| `A` | 65 | 01000001 | `k` | 01101011 | 00101010 | `2A` |
| `L` | 76 | 01001100 | `9` | 00111001 | 01110101 | `75` |
| `O` | 79 | 01001111 | `#` | 00100011 | 01101100 | `6C` |

- **Ciphertext (Hex):** `102A756C`

Simulasi Dekripsi (baris pertama): $00010000 \oplus 01011000 = 01001000 = 72 \rightarrow$ `H` (pulih sempurna).

### 3.4 Catatan Implementasi
Aplikasi ini menolak kunci yang panjangnya tidak sama dengan panjang pesan (dalam byte), dan menyediakan pembangkit kunci acak berbasis modul `secrets` (CSPRNG). Keluaran ditampilkan dalam heksadesimal karena hasil XOR dapat berupa byte yang tidak bisa dicetak.

---

## 4. LFSR-based Stream Cipher (Modern - Stream Simetris)

### 4.1 Teori Dasar
OTP tidak praktis karena kunci harus sepanjang pesan dan didistribusikan secara aman. Sandi aliran modern mengatasinya dengan **pembangkit keystream pseudo-acak (PRNG)**: kunci pendek (*seed*) diperluas menjadi aliran bit panjang yang tampak acak, lalu di-XOR dengan plaintext seperti pada Vernam.

**LFSR (*Linear Feedback Shift Register*)** adalah register geser $n$ bit yang bit masukannya berasal dari XOR beberapa bit tertentu (*tap*) pada register itu sendiri. LFSR mudah diimplementasikan di perangkat keras dan menghasilkan barisan bit berperiode panjang jika tap-nya dipilih dari polinomial primitif.

### 4.2 Formulasi Matematika
Pada implementasi ini (Fibonacci LFSR, geser ke kanan):
- **Bit output:** bit paling kanan (LSB) register.
- **Bit feedback:** $f = \bigoplus_{t \in T} b_{n-t}$, XOR bit-bit pada posisi tap $T$.
- **Update register:** geser satu bit ke kanan, lalu $f$ dimasukkan ke posisi paling kiri.
- **Keystream byte:** 8 bit output berurutan dikumpulkan menjadi 1 byte (bit pertama = MSB).
- **Enkripsi/Dekripsi:** $C_i = P_i \oplus KS_i$ dan $P_i = C_i \oplus KS_i$.

Polinomial umpan balik yang dipakai (semuanya primitif sehingga periodenya maksimum $2^n - 1$):

| Register | Polinomial | Tap | Periode |
| :---: | :--- | :---: | :---: |
| 4 bit | $x^4 + x^3 + 1$ | 4, 3 | 15 |
| 8 bit | $x^8 + x^6 + x^5 + x^4 + 1$ | 8, 6, 5, 4 | 255 |
| 16 bit | $x^{16} + x^{14} + x^{13} + x^{11} + 1$ | 16, 14, 13, 11 | 65.535 |

Seed tidak boleh semua nol karena register akan macet pada state `0000...` (feedback selalu 0).

### 4.3 Contoh Perhitungan Manual
- **Register:** 4 bit, tap 4 dan 3 (bit indeks 0 dan 1 dari kanan), **seed** = `1001`.
- Bit output = bit paling kanan; feedback = bit ke-4 dari kiri XOR bit ke-3 dari kiri.

| Clock | State | Feedback | Output | State Berikutnya |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 1001 | 1 $\oplus$ 0 = 1 | 1 | 1100 |
| 2 | 1100 | 0 $\oplus$ 0 = 0 | 0 | 0110 |
| 3 | 0110 | 0 $\oplus$ 1 = 1 | 0 | 1011 |
| 4 | 1011 | 1 $\oplus$ 1 = 0 | 1 | 0101 |
| 5 | 0101 | 1 $\oplus$ 0 = 1 | 1 | 1010 |
| 6 | 1010 | 0 $\oplus$ 1 = 1 | 0 | 1101 |
| 7 | 1101 | 1 $\oplus$ 0 = 1 | 1 | 1110 |
| 8 | 1110 | 0 $\oplus$ 1 = 1 | 0 | 1111 |

Keystream byte pertama = bit output clock 1-8 = `10011010` = `9A`.

Enkripsi huruf `K` (ASCII 75 = `01001011`):
$$01001011 \oplus 10011010 = 11010001 = \text{D1}$$

Setelah 15 clock state kembali ke `1001` (periode = $2^4 - 1 = 15$), sehingga keystream byte kedua dilanjutkan dari clock 9 dst. Untuk `KR` dengan seed `1001` hasilnya `D1A3`. Dekripsi menghasilkan keystream yang identik dari seed yang sama.

### 4.4 Catatan Keamanan
LFSR bersifat **linear**: dengan $2n$ bit keystream yang diketahui, algoritma Berlekamp-Massey dapat merekonstruksi seluruh register. Karena itu LFSR murni tidak aman untuk penggunaan nyata; sistem praktis (mis. A5/1, E0) menggabungkan beberapa LFSR dengan fungsi non-linear. Aplikasi ini memakai LFSR tunggal untuk tujuan edukatif.

---

## 5. Super Enkripsi (Hybrid Cryptosystem)

### 5.1 Filosofi Desain (Defense in Depth)
Prinsip *Defense in Depth* dalam kriptografi menyatakan bahwa sistem keamanan yang menggabungkan beberapa lapisan perlindungan independen akan meminimalkan risiko kerentanan tunggal (*single point of failure*).
Super Enkripsi memadukan properti:
1. **Difusi Awal (Playfair):** Menghancurkan pola bigram bahasa alami.
2. **Konfusi Polialfabetik (Vigenère):** Menghilangkan keseragaman frekuensi karakter tunggal.
3. **Keystream Pseudo-Acak (LFSR Stream Cipher):** Mengubah teks huruf menjadi byte biner yang tampak acak dengan XOR terhadap keystream dari seed.
4. **Kerahasiaan Sempurna Berbasis Kunci Acak (Vernam/OTP):** Lapisan terakhir dengan kunci acak sepanjang data.

### 5.2 Aliran Data dan Normalisasi Format Antar-Tahap
Salah satu tantangan utama dalam *cipher chaining* adalah memastikan kompatibilitas format data saat berpindah antar algoritma tanpa mengalami kehilangan data (*data loss*):

1. **Tahap 1 (Playfair):**
   - Masukan: Plaintext string.
   - Normalisasi: Huruf non-alfabet disaring, huruf $J \rightarrow I$, huruf kembar disisipkan $X$.
   - Keluaran ($C_1$): String alfabet berpasangan genap hasil transformasi matriks $5 \times 5$.
2. **Tahap 2 (Vigenère):**
   - Masukan: String $C_1$ (huruf kapital A-Z).
   - Keluaran ($C_2$): String teks tergeser secara modular.
3. **Tahap 3 (LFSR Stream Cipher):**
   - Masukan: String $C_2$ dikonversi ke byte.
   - Pemrosesan: Setiap byte di-XOR dengan keystream byte dari register LFSR.
   - Keluaran ($C_3$): Deretan byte biner (ditampilkan sebagai heksadesimal, tetapi diteruskan sebagai byte mentah ke tahap berikutnya).
4. **Tahap 4 (Vernam / OTP):**
   - Masukan: Byte $C_3$.
   - Pemrosesan: Setiap byte di-XOR dengan kunci OTP acak yang panjangnya sama dengan $C_3$ (dibangkitkan otomatis atau diisi manual).
   - Keluaran ($C_{\text{final}}$): String **heksadesimal**. Format heksadesimal dipilih karena hasil XOR berupa byte yang tidak selalu dapat dicetak, sedangkan heksadesimal aman disalin dan ditransmisikan.

**Mengapa Playfair di tahap pertama?** Playfair menggabungkan $J$ dan $I$. Jika Playfair dijalankan setelah Vigenère, huruf $J$ yang kebetulan muncul pada ciphertext Vigenère akan berubah menjadi $I$ dan tidak dapat dipulihkan saat dekripsi. Dengan menjalankan Playfair lebih dulu, penggabungan $J \rightarrow I$ dan penghapusan spasi hanya terjadi pada plaintext asli (sifat bawaan Playfair), sementara tahap-tahap sesudahnya (Vigenère, LFSR, Vernam) bersifat invertibel penuh.

### 5.3 Pembalikan Dekripsi yang Presisi
Proses dekripsi menerapkan prinsip operasi invers secara simetris terbalik:
$$C_{\text{final}} \xrightarrow{\text{Vernam}^{-1}} C_3 \xrightarrow{\text{LFSR}^{-1}} C_2 \xrightarrow{\text{Vigenère}^{-1}} C_1 \xrightarrow{\text{Playfair}^{-1}} \text{Plaintext (tanpa spasi, dengan X padding)}$$
Setiap kunci yang digunakan harus identik dengan kunci saat enkripsi (termasuk kunci Vernam yang dibangkitkan otomatis, yang wajib disimpan), dan urutan pembalikan tidak boleh tertukar.

Karena sifat Playfair, plaintext hasil pemulihan tidak mengandung spasi, $J$ tergantikan $I$, dan dapat memiliki huruf $X$ tambahan sebagai padding (contoh: `KRIPTOGRAFI MODERN` menjadi `KRIPTOGRAFIMODERNX` atau sejenisnya).
