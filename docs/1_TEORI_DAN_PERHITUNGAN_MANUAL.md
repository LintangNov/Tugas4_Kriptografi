# Panduan Teori Dasar dan Perhitungan Manual Algoritma Kriptografi

Dokumen ini disusun sebagai referensi akademis komprehensif bagi tim pengembang untuk memahami prinsip teoritis, formulasi matematika, dan simulasi perhitungan manual dari seluruh algoritma yang diimplementasikan dalam aplikasi: Vigenère Cipher, Playfair Cipher, AES-128, RSA, serta Super Enkripsi.

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

## 3. Advanced Encryption Standard / AES-128 (Modern - Simetris)

### 3.1 Teori Dasar
AES (Rijndael) adalah sandi blok simetris standar FIPS PUB 197 yang beroperasi pada blok berukuran tetap 128 bit (16 byte). Untuk AES-128, panjang kunci adalah 128 bit dengan 10 putaran (*round*). Struktur AES berbasis *Substitution-Permutation Network* (SPN), bukan struktur Feistel.

Blok 16 byte disusun dalam Matriks State $4 \times 4$ berordo kolom (*column-major order*):
```
| b0  b4  b8  b12 |
| b1  b5  b9  b13 |
| b2  b6  b10 b14 |
| b3  b7  b11 b15 |
```

### 3.2 Tahapan Algoritma AES
1. **Padding (PKCS#7):**
   Setiap blok masukan harus tepat kelipatan 16 byte. Jika panjang data modulo 16 menyisakan $k$ byte ($k < 16$), maka ditambahkan $16 - k$ byte padding, di mana nilai masing-masing byte padding adalah bilangan $(16 - k)$. Jika data sudah tepat kelipatan 16 byte, tetap ditambahkan satu blok penuh berukuran 16 byte bernilai `0x10`.
2. **Key Expansion:**
   Kunci 16 byte diekspansi menjadi deretan *Round Keys* (11 sub-kunci untuk AES-128, yaitu Round 0 hingga Round 10). Pembangkitan melibatkan operasi `RotWord`, `SubWord` (S-Box), dan penambahan konstanta putaran `Rcon`.
3. **Struktur Putaran:**
   - **Pre-Round (Round 0):** `AddRoundKey`
   - **Round 1 sampai Round 9 (Standard Round):**
     1. `SubBytes`: Substitusi byte non-linear menggunakan S-Box Rijndael.
     2. `ShiftRows`: Pergeseran siklis ke kiri pada setiap baris matriks state:
        - Baris 0: tidak bergeser.
        - Baris 1: bergeser 1 byte ke kiri.
        - Baris 2: bergeser 2 byte ke kiri.
        - Baris 3: bergeser 3 byte ke kiri.
     3. `MixColumns`: Operasi difusi linear di mana setiap kolom dikalikan dengan matriks konstan terbalikkan dalam medan berhingga (*Galois Field*) $GF(2^8)$ modulo polinomial tak tereduksi:
        $$m(x) = x^8 + x^4 + x^3 + x + 1 \quad (\text{heksadesimal: } \text{0x11B})$$
     4. `AddRoundKey`: Operasi XOR bitwise antara State Matrix dengan Round Key putaran terkait.
   - **Round 10 (Final Round):**
     Sama seperti standard round, namun **tanpa operasi MixColumns** (`SubBytes` -> `ShiftRows` -> `AddRoundKey`). Hal ini dirancang agar proses enkripsi dan dekripsi memiliki simetri struktural.

### 3.3 Operasi Perkalian pada Galois Field GF(2^8) (xtime)
Pada tahap `MixColumns`, perkalian dengan bilangan 2 dilakukan melalui fungsi `xtime(a)`:
- Geser bit ke kiri 1 posisi: `a << 1`.
- Jika bit ke-7 bernilai 1 (terjadi overflow di luar 8 bit), lakukan XOR dengan `0x1B`.
Contoh perkalian:
- $2 \cdot a = \text{xtime}(a)$
- $3 \cdot a = \text{xtime}(a) \oplus a$

---

## 4. Rivest-Shamir-Adleman / RSA (Modern - Asimetris)

### 4.1 Teori Dasar & Teorema Euler
RSA didasarkan pada prinsip matematika bahwa perkalian dua bilangan prima besar adalah komputasi yang sangat cepat, namun memfaktorkan kembali hasil kali tersebut menjadi komponen primanya (*integer factorization problem*) adalah komputasi yang sangat sulit dalam waktu polinomial.

Teorema Euler menyatakan bahwa jika $\gcd(a, n) = 1$, maka:
$$a^{\phi(n)} \equiv 1 \pmod n$$
Hal ini berimplikasi bahwa:
$$a^{k \cdot \phi(n) + 1} \equiv a \pmod n$$

### 4.2 Langkah Pembentukan Kunci (Key Generation)
1. Pilih dua bilangan prima sembarang $p$ dan $q$ ($p \ne q$).
2. Hitung modulus:
   $$n = p \times q$$
3. Hitung fungsi Euler Totient:
   $$\phi(n) = (p - 1)(q - 1)$$
4. Tentukan eksponen publik $e$ dengan ketentuan:
   $$1 < e < \phi(n) \quad \text{dan} \quad \gcd(e, \phi(n)) = 1$$
5. Tentukan eksponen privat $d$ sebagai invers perkalian modular dari $e$ modulo $\phi(n)$:
   $$e \cdot d \equiv 1 \pmod{\phi(n)}$$
   Nilai $d$ dicari menggunakan Algoritma Euclidean Diperluas (*Extended Euclidean Algorithm*).
6. **Kunci Publik:** $(e, n)$
7. **Kunci Privat:** $(d, n)$

### 4.3 Formulasi Enkripsi dan Dekripsi
- **Enkripsi:**
  $$C = M^e \pmod n$$
  Syarat batas matematis: Nilai integer pesan $M$ harus lebih kecil dari modulus $n$ ($M < n$).
- **Dekripsi:**
  $$M = C^d \pmod n$$

### 4.4 Contoh Perhitungan Manual
- Pilih $p = 61$, $q = 53$.
- Modulus $n = 61 \times 53 = 3233$.
- Totient $\phi(n) = (61 - 1)(53 - 1) = 60 \times 52 = 3120$.
- Pilih $e = 17$.
  Verifikasi: $\gcd(17, 3120) = 1$ (karena $3120 = 17 \times 183 + 9$, $\gcd(17, 9) = 1$).
- Hitung $d$:
  Mencari $d$ sedemikian rupa sehingga $17 \cdot d \equiv 1 \pmod{3120}$.
  Dengan Extended Euclidean Algorithm didapatkan $d = 2753$.
  Pembuktian: $17 \times 2753 = 46801 = 15 \times 3120 + 1 \equiv 1 \pmod{3120}$.

Simulasi Enkripsi Karakter:
- Karakter pesan: `'A'` $\rightarrow$ ASCII $M = 65$.
- Enkripsi:
  $$C = 65^{17} \pmod{3233}$$
  Menggunakan metode *repeated squaring*:
  $$65^2 = 4225 \equiv 992 \pmod{3233}$$
  $$65^4 = 992^2 = 984064 \equiv 1374 \pmod{3233}$$
  $$65^8 = 1374^2 = 1887876 \equiv 3053 \pmod{3233}$$
  $$65^{16} = 3053^2 = 9320809 \equiv 992 \pmod{3233}$$
  $$C = 65^{17} = 65^{16} \times 65 = 992 \times 65 = 64480 \equiv 3013 \pmod{3233}$$
  Ciphertext numerik: `3013`.

Simulasi Dekripsi:
- $$M = 3013^{2753} \pmod{3233} = 65 \rightarrow \text{karakter } 'A' \text{ (pulih sempurna)}.$$

---

## 5. Super Enkripsi (Hybrid Cryptosystem)

### 5.1 Filosofi Desain (Defense in Depth)
Prinsip *Defense in Depth* dalam kriptografi menyatakan bahwa sistem keamanan yang menggabungkan beberapa lapisan perlindungan independen akan meminimalkan risiko kerentanan tunggal (*single point of failure*).
Super Enkripsi memadukan properti:
1. **Difusi Awal (Playfair):** Menghancurkan pola bigram bahasa alami.
2. **Konfusi Polialfabetik (Vigenère):** Menghilangkan keseragaman frekuensi karakter tunggal.
3. **Difusi Tingkat Tinggi & Kompleksitas Non-Linear (AES-128):** Menerapkan standar enkripsi blok simetris terkuat terhadap kriptanalisis diferensial dan linier.
4. **Asimetri Kunci Publik (RSA):** Memberikan proteksi enkripsi modular berbasis kesulitan faktorisasi prima.

### 5.2 Aliran Data dan Normalisasi Format Antar-Tahap
Salah satu tantangan utama dalam *cipher chaining* adalah memastikan kompatibilitas format data saat berpindah antar algoritma tanpa mengalami kehilangan data (*data loss*):

1. **Tahap 1 (Vigenère):**
   - Masukan: Plaintext string UTF-8.
   - Keluaran ($C_1$): String teks tergeser secara modular.
2. **Tahap 2 (Playfair):**
   - Masukan: String $C_1$.
   - Normalisasi: Huruf non-alfabet disaring, huruf $J \rightarrow I$, huruf kembar disisipkan $X$.
   - Keluaran ($C_2$): String alfabet berpasangan genap hasil transformasi matriks $5 \times 5$.
3. **Tahap 3 (AES-128):**
   - Masukan: String $C_2$ (dikonversi ke raw byte array UTF-8).
   - Pemrosesan: Ditambahkan padding PKCS#7 agar kelipatan 16 byte, lalu dienkripsi menggunakan AES mode ECB.
   - Keluaran ($C_3$): String **Base64**. Format Base64 dipilih karena menghasilkan string teks ASCII bersih dan aman ditransmisikan tanpa risiko byte biner tak tampak (*non-printable characters*).
4. **Tahap 4 (RSA):**
   - Masukan: String Base64 $C_3$.
   - Pemrosesan: Setiap karakter ASCII dari string Base64 (yang memiliki nilai numerik $0 \le M \le 127 < n$) dienkripsi satu per satu menggunakan $C = M^e \pmod n$.
   - Keluaran ($C_{\text{final}}$): Deretan integer yang dipisahkan oleh spasi.

### 5.3 Pembalikan Dekripsi yang Presisi
Proses dekripsi menerapkan prinsip operasi invers secara simetris terbalik:
$$C_{\text{final}} \xrightarrow{\text{RSA Decrypt}} C_3 \text{ (Base64)} \xrightarrow{\text{AES Decrypt}} C_2 \xrightarrow{\text{Playfair Decrypt}} C_1 \xrightarrow{\text{Vigenère Decrypt}} \text{Plaintext Asli}$$
Setiap kunci yang digunakan harus identik dengan kunci saat enkripsi, dan urutan pembalikan tidak boleh tertukar.
