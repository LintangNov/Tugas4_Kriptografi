# Panduan Tanya Jawab Ujian Presentasi Kriptografi

Dokumen ini disusun khusus sebagai persiapan menghadapi sesi tanya jawab kritis dan pengujian dari dosen pengampu mata kuliah Kriptografi. Jawaban disusun secara lugas, akademis, dan berbasis prinsip ilmu kriptografi.

---

## Bagian 1: Konsep Dasar & Sandi Klasik (Vigenère & Playfair)

### Q1: Apa perbedaan mendasar antara sandi monoalfabetik dan polialfabetik?
**Jawaban:**
- **Monoalfabetik:** Setiap satu huruf pada plaintext selalu dipetakan ke huruf ciphertext yang sama sepanjang pesan (misal: Caesar Cipher). Kelemahan utamanya adalah rentan terhadap *Frequency Analysis* (analisis frekuensi kemunculan huruf bahasa alami, seperti huruf 'E' atau 'A' yang frekuensinya dominan).
- **Polialfabetik:** Satu huruf plaintext dapat dipetakan ke berbagai huruf ciphertext yang berbeda tergantung pada posisi karakter dan huruf kunci yang bersesuaian (seperti pada Vigenère Cipher). Hal ini meratakan distribusi frekuensi kemunculan huruf sehingga kriptanalisis frekuensi huruf tunggal tidak lagi efektif.

### Q2: Jika Vigenère kebal terhadap analisis frekuensi sederhana, bagaimana cara membobolnya?
**Jawaban:**
Vigenère dapat dipecahkan melalui dua pendekatan klasik:
1. **Uji Kasiski (Kasiski Examination):** Mencari pola kata atau trigram yang berulang pada ciphertext, lalu menghitung selisih jarak (*distance*) antar kemunculan pola tersebut. Faktor persekutuan terbesar (FPB/GCD) dari jarak-jarak tersebut kemungkinan besar adalah panjang kunci ($m$).
2. **Indeks Koinsidensi (Index of Coincidence - Friedman Test):** Menghitung probabilitas dua huruf yang dipilih secara acak dari teks adalah sama.
Setelah panjang kunci ($m$) diketahui, ciphertext dapat dipecah menjadi $m$ kelompok sandi Caesar monoalfabetik independen, yang kemudian dapat diselesaikan dengan analisis frekuensi standar.

### Q3: Mengapa Playfair Cipher menggunakan matriks 5x5 dan bukan 6x6?
**Jawaban:**
Alfabet standar bahasa Inggris berjumlah 26 huruf. Matriks $5 \times 5$ menyediakan 25 sel, sehingga satu huruf harus dilebur (standar historisnya adalah menggabungkan `I` dan `J` karena keduanya memiliki kemiripan bunyi dan bentuk penulisan dalam bahasa Latin).
Matriks $6 \times 6$ (36 sel) sebenarnya bisa dibuat untuk menampung 26 huruf alfabet ditambah angka 0-9. Namun, tujuan utama Playfair historis adalah mengenkripsi teks telegraf huruf, sehingga matriks $5 \times 5$ menjadi standar baku Playfair di literatur kriptografi.

### Q4: Mengapa pada Playfair huruf kembar dalam satu pasangan disisipkan 'X'? Apa yang terjadi jika tidak disisipkan?
**Jawaban:**
Jika sepasang huruf bernilai sama (misal: `EE`), kedua huruf tersebut berada pada posisi baris dan kolom yang identik di matriks. Akibatnya:
- Aturan baris sama, kolom sama, maupun persegi panjang tidak dapat diterapkan secara bermakna (membentuk geometri degenerasi).
- Oleh karena itu, aturan baku Playfair mewajibkan penyisipan huruf pengisi (*null letter*), biasanya `X`, di antara huruf kembar tersebut sehingga menjadi `EX` dan pasangan berikutnya diawali huruf `E` yang kedua.

---

## Bagian 2: Kriptografi Modern (AES-128)

### Q5: Mengapa AES-128 menggunakan 10 putaran (rounds)? Mengapa tidak 1 putaran saja?
**Jawaban:**
Satu putaran AES belum memberikan difusi dan konfusi yang memadai.
- **Konsep Claude Shannon:** Keamanan sandi blok bergantung pada dua properti, yaitu *Confusion* (mengaburkan hubungan antara kunci dan ciphertext) dan *Diffusion* (menyebarkan pengaruh satu bit plaintext ke seluruh ciphertext — fenomena *Avalanche Effect*).
- Pada AES, dibutuhkan minimal 4 putaran agar 1 perubahan bit pada plaintext atau kunci mempengaruhi seluruh 128 bit matriks state (*full diffusion*). Putaran sisanya (hingga 10 putaran pada AES-128) berfungsi memberikan *security margin* matematis terhadap serangan kriptanalisis canggih seperti *Linear Cryptanalysis* dan *Differential Cryptanalysis*.

### Q6: Jelaskan fungsi masing-masing 4 transformasi pada putaran AES! Mana yang menyediakan Confusion dan mana yang Diffusion?
**Jawaban:**
1. **`SubBytes` (Confusion):** Substitusi byte non-linear menggunakan S-Box. S-Box Rijndael dibentuk dari invers perkalian dalam medan berhingga $GF(2^8)$ diikuti transformasi afin. Ini adalah satu-satunya komponen non-linear pada AES yang mencegah serangan berbasis aljabar linier.
2. **`ShiftRows` (Diffusion):** Permutasi byte linear melalui pergeseran baris matriks state secara siklis ke kiri. Memastikan byte-byte pada kolom yang sama tersebar ke kolom-kolom yang berbeda pada putaran berikutnya.
3. **`MixColumns` (Diffusion):** Operasi difusi kolom berbasis perkalian matriks dalam $GF(2^8)$. Setiap byte hasil transformasi dipengaruhi oleh keempat byte pada kolom sebelumnya.
4. **`AddRoundKey`:** Operasi XOR antara matriks state dengan Round Key putaran terkait untuk memasukkan entropi kunci rahasia ke dalam blok data.

### Q7: Mengapa pada Round 10 operasi MixColumns dihilangkan?
**Jawaban:**
MixColumns sengaja dihilangkan pada putaran terakhir (Round 10) semata-mata untuk menjaga simetri struktural arsitektur enkripsi dan dekripsi. Penghilangan ini tidak mengurangi keamanan algoritma karena ciphertext langsung di-XOR dengan sub-kunci terakhir (`AddRoundKey`), namun mempermudah desain sirkuit perangkat keras (*hardware*) dan komputasi prosesor agar modul dekripsi dapat menggunakan alur yang setara dengan enkripsi.

### Q8: Mengapa menggunakan perkalian pada Galois Field GF(2^8) pada MixColumns dan bukan perkalian integer biasa?
**Jawaban:**
Dalam aritmatika integer biasa, perkalian dua bilangan 8-bit ($0 - 255$) dapat menghasilkan nilai hingga 16-bit ($0 - 65025$), yang menyebabkan terjadinya pertambahan ukuran (*data expansion*) atau kehilangan data jika dipotong modulo 256 biasa (karena modulo 256 tidak membentuk *field* pembagian; tidak semua elemen memiliki invers perkalian).
Dalam Medan Galois $GF(2^8)$ dengan polinomial tak tereduksi $x^8 + x^4 + x^3 + x + 1$:
1. Hasil operasi tertutup sempurna selalu berada dalam rentang tepat 1 byte ($0 - 255$).
2. Setiap elemen non-nol dijamin memiliki invers perkalian unik, sehingga operasi matriks MixColumns dapat dibalik (*invertible*) secara presisi saat proses dekripsi (`InvMixColumns`).

### Q9: Mengapa untuk visualisasi blok dipilih mode ECB? Apa kelemahan ECB pada sistem produksi nyata?
**Jawaban:**
- **Tujuan Demonstrasi Edukatif:** Mode ECB (*Electronic Codebook*) dipilih karena setiap blok 16 byte dienkripsi secara independen, sehingga mahasiswa dan dosen dapat menelusuri transformasi State Matrix $4 \times 4$ untuk blok pertama secara deterministik tanpa ketergantungan pada nilai Initialization Vector (IV) blok lain.
- **Kelemahan Produksi:** ECB tidak menyembunyikan pola data. Blok plaintext yang identik akan selalu menghasilkan blok ciphertext yang identik jika menggunakan kunci yang sama (contoh klasik: gambar *ECB Penguin* yang siluetnya tetap terlihat jelas). Untuk produksi nyata, wajib menggunakan mode yang memiliki rantai ketergantungan antar-blok seperti CBC (*Cipher Block Chaining*) atau GCM (*Galois/Counter Mode*).

---

## Bagian 3: Kriptografi Asimetris (RSA)

### Q10: Mengapa mencari nilai d menggunakan modulo phi(n) dan bukan modulo n?
**Jawaban:**
Ini bersumber langsung dari **Teorema Euler**:
Jika $\gcd(M, n) = 1$, maka:
$$M^{\phi(n)} \equiv 1 \pmod n$$
Oleh karena itu, jika kita mengalikan eksponen sebanyak kelipatan $\phi(n)$:
$$M^{k \cdot \phi(n) + 1} \equiv (M^{\phi(n)})^k \cdot M \equiv 1^k \cdot M \equiv M \pmod n$$
Kita menginginkan proses dekripsi mengembalikan pesan asli:
$$(M^e)^d = M^{e \cdot d} \equiv M \pmod n$$
Maka eksponen harus memenuhi persamaan:
$$e \cdot d = k \cdot \phi(n) + 1 \iff e \cdot d \equiv 1 \pmod{\phi(n)}$$
Oleh sebab itu, hubungan invers antara $e$ dan $d$ beroperasi di dalam modulo grup totient $\phi(n)$, bukan modulo $n$.

### Q11: Mengapa eksponen publik e harus relatif prima dengan phi(n)?
**Jawaban:**
Nilai $d$ adalah invers perkalian modular dari $e$ modulo $\phi(n)$. Berdasarkan teori bilangan (Identitas Bézout), invers modular $d$ sedemikian rupa sehingga $e \cdot d \equiv 1 \pmod{\phi(n)}$ hanya ada jika dan hanya jika $\gcd(e, \phi(n)) = 1$. Jika $e$ dan $\phi(n)$ memiliki faktor persekutuan lebih besar dari 1, maka invers modular tidak terdefinisi dan kunci privat $d$ tidak dapat ditemukan.

### Q12: Apa batasan matematis nilai pesan M pada RSA?
**Jawaban:**
Dalam RSA, operasi aritmatika dilakukan di dalam ring integer $\mathbb{Z}_n$. Oleh karena itu, nilai numerik pesan $M$ harus secara mutlak lebih kecil dari nilai modulus $n$ ($0 \le M < n$).
Jika $M \ge n$, operasi $M \pmod n$ akan memotong nilai $M$, sehingga proses dekripsi $C^d \pmod n$ hanya akan mengembalikan nilai $M \pmod n$, bukan nilai asli $M$.

### Q13: Mengapa implementasi RSA di program ini menggunakan prima kecil dan bukan standar 2048-bit?
**Jawaban:**
Implementasi RSA dalam aplikasi ini ditujukan untuk **visualisasi pendidikan langkah demi langkah** (*transparent white-box tracing*). Jika menggunakan bilangan prima 2048-bit (sekitar 617 digit desimal), proses perhitungan Extended Euclidean dan perpangkatan modular karakter tidak dapat ditampilkan secara visual dalam tabel interaktif. Di halaman aplikasi telah disertakan kotak *disclaimer* resmi yang menegaskan bahwa implementasi ini adalah untuk demo edukatif, sedangkan implementasi industri wajib menggunakan panjang kunci $\ge 2048$ bit dan skema padding probabilitik OAEP.

---

## Bagian 4: Arsitektur Super Enkripsi

### Q14: Apakah menggabungkan beberapa cipher (cipher chaining) selalu menjamin keamanan yang lebih kuat?
**Jawaban:**
Tidak selalu secara otomatis. Dalam kriptografi teoritis, terdapat beberapa prinsip terkait kombinasi cipher:
1. Jika salah satu cipher merupakan pemetaan kelompok (*group*) tertutup, kombinasi dua fungsi tidak menambah ukuran ruang kunci (contoh: mengenkripsi Caesar dua kali dengan pergeseran 3 dan 5 sama saja dengan satu kali Caesar pergeseran 8).
2. Namun, dalam kasus **Super Enkripsi** di proyek ini, keempat algoritma memiliki paradigma matematika yang sama sekali berbeda:
   - Vigenère: Substitusi polialfabetik.
   - Playfair: Substitusi bigram non-linear pada kisi $5 \times 5$.
   - AES: Jaringan SPN permutasi-substitusi pada medan Galois.
   - RSA: Perpangkatan modular grup bilangan prima.
   Kombinasi ini tidak membentuk struktur grup tertutup, sehingga menghasilkan lapisan pertahanan berlapis (*Defense in Depth*) yang saling melengkapi.

### Q15: Apa itu serangan Meet-in-the-Middle dan apakah mengancam skema Super Enkripsi kita?
**Jawaban:**
- **Definisi:** Serangan *Meet-in-the-Middle* (MitM) adalah serangan ruang-waktu (*time-space tradeoff*) terhadap enkripsi berganda di mana penyerang mengenkripsi plaintext dari sisi kiri dan mendekripsi ciphertext dari sisi kanan secara simultan, lalu mencari titik temu (*collision*) pada tabel penyimpanan perantara (seperti yang mereduksi keamanan Double-DES dari $2^{112}$ menjadi $2^{57}$).
- **Relevansi:** Serangan MitM membutuhkan pasangan plaintext-ciphertext yang diketahui (*Known-Plaintext Attack*) dan ruang penyimpanan memori yang sangat besar. Pada skema kita yang mengikutsertakan AES-128 (ruang kunci $2^{128}$) dan RSA, kompleksitas ruang dan komputasi untuk menyimpan kondisi perantara di level AES dan RSA berada di luar batas komputasi praktis dunia nyata.

### Q16: Mengapa urutan dekripsi pada Super Enkripsi harus dibalik secara tepat (RSA -> AES -> Playfair -> Vigenere)?
**Jawaban:**
Operasi enkripsi berantai merupakan komposisi fungsi matematika:
$$C_{\text{final}} = f_4(f_3(f_2(f_1(P))))$$
Berdasarkan sifat aljabar fungsi komposisi terbalikkan (*invertible composition*), invers dari komposisi fungsi adalah kebalikan dari urutan invers masing-masing fungsi:
$$(f_4 \circ f_3 \circ f_2 \circ f_1)^{-1} = f_1^{-1} \circ f_2^{-1} \circ f_3^{-1} \circ f_4^{-1}$$
Artinya, fungsi yang diterapkan terakhir ($f_4$ = RSA) harus dibalik paling pertama ($f_4^{-1}$), diikuti $f_3^{-1}$ (AES), $f_2^{-1}$ (Playfair), dan terakhir $f_1^{-1}$ (Vigenère). Jika urutan ini diubah, data biner yang dihasilkan akan menjadi derau acak (*garbage data*) dan gagal dipulihkan.
