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

## Bagian 2: Kriptografi Modern - Vernam Cipher (One-Time Pad)

### Q5: Mengapa Vernam Cipher / One-Time Pad disebut aman secara sempurna (*perfect secrecy*)?
**Jawaban:**
- **Konsep Shannon (1949):** Sebuah sandi memiliki *perfect secrecy* jika ciphertext tidak memberikan informasi apa pun tentang plaintext, yaitu $P(M \mid C) = P(M)$.
- Pada OTP, untuk ciphertext $C$ yang sama, setiap plaintext dengan panjang yang sama dapat dihasilkan oleh suatu kunci tertentu ($K = C \oplus M$), dan semua kunci sama-sama mungkin. Penyerang tidak bisa membedakan plaintext yang benar dari yang salah, sehingga *brute force* pun tidak berguna.
- Syarat mutlaknya: kunci acak sejati, panjang kunci sama dengan pesan, dan kunci tidak boleh dipakai ulang.

### Q6: Apa yang terjadi jika kunci OTP dipakai dua kali (*two-time pad*)?
**Jawaban:**
Jika dua pesan $P_1$ dan $P_2$ dienkripsi dengan kunci $K$ yang sama, maka:
$$C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2$$
Kunci hilang dari persamaan, dan penyerang memperoleh XOR kedua plaintext yang dapat dipecahkan dengan analisis frekuensi/*crib dragging*. Inilah alasan kunci OTP harus sekali pakai. Pada aplikasi kami, kunci dibangkitkan baru setiap enkripsi (opsi acak otomatis).

### Q7: Jika OTP aman sempurna, mengapa tidak dipakai di mana-mana?
**Jawaban:**
- **Panjang kunci = panjang pesan**, sehingga pesan 1 GB butuh kunci 1 GB.
- **Distribusi kunci** harus lewat saluran yang benar-benar aman, padahal masalah itu yang ingin diselesaikan oleh kriptografi.
- **Pembangkit acak sejati** sulit didapat; PRNG biasa tidak memenuhi syarat teori (hanya *computationally secure*).
- Tidak ada perlindungan integritas: penyerang yang tahu plaintext dapat mengubah bit ciphertext dan mengubah plaintext secara terarah (*malleability*).

### Q8: Mengapa operasi enkripsi dan dekripsi Vernam identik?
**Jawaban:**
Karena XOR adalah operasi yang menjadi invers dirinya sendiri: $(P \oplus K) \oplus K = P$. Ini juga sebabnya di kode kami satu fungsi `vernam_xor_bytes` dipakai untuk enkripsi dan dekripsi.

### Q9: Mengapa aplikasi menampilkan ciphertext dalam heksadesimal dan kunci dibatasi karakter tercetak?
**Jawaban:**
- Hasil XOR dua byte ASCII dapat menghasilkan byte kontrol (mis. `0x10`) yang tidak bisa dicetak atau disalin dengan aman; heksadesimal memetakan tiap byte ke dua karakter yang aman.
- Kunci acak dibangkitkan dari huruf dan angka (62 simbol) agar mudah disalin untuk dekripsi. Konsekuensinya entropi per byte kunci $\log_2 62 \approx 5{,}95$ bit, bukan 8 bit penuh, sehingga secara ketat bukan OTP ideal. Ini kompromi antara kemudahan demo dan teori; kunci OTP produksi harus berupa byte acak penuh.

---

## Bagian 3: Kriptografi Modern - LFSR Stream Cipher

### Q10: Apa perbedaan Vernam/OTP dengan LFSR Stream Cipher?
**Jawaban:**
Keduanya meng-XOR plaintext dengan keystream ($C_i = P_i \oplus KS_i$). Bedanya pada sumber keystream: OTP memakai kunci acak sejati sepanjang pesan, sedangkan LFSR mengekspansi seed pendek (4/8/16 bit) menjadi keystream panjang secara deterministik. LFSR praktis (kunci pendek) tetapi hanya *computationally secure* dan pada bentuk linear murni tidak aman.

### Q11: Bagaimana cara kerja LFSR dan apa itu tap?
**Jawaban:**
LFSR adalah register geser $n$ bit. Setiap clock: (1) bit paling kanan dikeluarkan sebagai output, (2) bit-bit pada posisi tap di-XOR menjadi bit feedback, (3) register digeser satu bit ke kanan dan feedback dimasukkan dari kiri. Posisi tap menentukan polinomial umpan balik; misalnya tap 4 dan 3 pada register 4 bit sesuai dengan $x^4 + x^3 + 1$.

### Q12: Mengapa seed tidak boleh nol semua dan mengapa tap dipilih dari polinomial primitif?
**Jawaban:**
- **Seed nol:** feedback = XOR dari nol = 0, sehingga register tetap `000...0` selamanya dan keystream selalu 0, sehingga plaintext tidak terenkripsi sama sekali.
- **Polinomial primitif:** menjamin periode maksimum $2^n - 1$, yaitu register melewati seluruh state non-nol sebelum berulang. Pada demo: 4 bit periode 15, 8 bit periode 255, 16 bit periode 65.535 (sudah kami verifikasi lewat simulasi).

### Q13: Mengapa LFSR murni tidak aman? Bagaimana memecahkannya?
**Jawaban:**
LFSR bersifat **linear** atas GF(2). Jika penyerang mengetahui $2n$ bit keystream (mis. lewat *known-plaintext attack*, karena $KS = P \oplus C$), algoritma **Berlekamp-Massey** dapat menemukan polinomial umpan balik dan state register, sehingga seluruh keystream dapat diprediksi. Karena itu sistem nyata (A5/1, E0) memakai banyak LFSR dengan fungsi kombinasi non-linear atau *clock control*. Proyek kami memakai satu LFSR untuk tujuan edukatif.

### Q14: Mengapa seed LFSR pada dekripsi harus sama persis dengan saat enkripsi?
**Jawaban:**
Dekripsi membangkitkan keystream yang sama dari seed yang sama, lalu meng-XOR ciphertext. Seed berbeda menghasilkan keystream berbeda sehingga hasilnya derau. Sifat ini sekaligus alasan sandi aliran tidak boleh memakai ulang pasangan (seed, keystream) untuk dua pesan, karena $C_1 \oplus C_2 = P_1 \oplus P_2$ seperti pada *two-time pad*.

---

## Bagian 4: Arsitektur Super Enkripsi

### Q15: Apakah menggabungkan beberapa cipher (cipher chaining) selalu menjamin keamanan yang lebih kuat?
**Jawaban:**
Tidak selalu secara otomatis. Dalam kriptografi teoritis, terdapat beberapa prinsip terkait kombinasi cipher:
1. Jika salah satu cipher merupakan pemetaan kelompok (*group*) tertutup, kombinasi dua fungsi tidak menambah ukuran ruang kunci (contoh: mengenkripsi Caesar dua kali dengan pergeseran 3 dan 5 sama saja dengan satu kali Caesar pergeseran 8).
2. Pada **Super Enkripsi** di proyek ini, terdapat dua pasang lapisan yang perlu dicermati:
   - Playfair: substitusi bigram non-linear pada kisi $5 \times 5$.
   - Vigenère: substitusi polialfabetik.
   - LFSR dan Vernam: keduanya berupa XOR terhadap keystream. **Secara matematis, XOR dua keystream berurutan sama saja dengan XOR sekali dengan keystream gabungan** ($P \oplus KS_1 \oplus K_2 = P \oplus (KS_1 \oplus K_2)$), sehingga kedua lapisan ini setara satu sandi aliran dengan kunci efektif $KS_1 \oplus K_2$.
   Keamanan lapisan XOR gabungan itu setidaknya sekuat lapisan terkuatnya: karena kunci Vernam acak dan sepanjang pesan, penyerang tidak dapat memulihkan keystream LFSR maupun plaintext tanpa kunci Vernam tersebut. Jadi lapisan LFSR di dalamnya tidak menambah kekuatan teoretis di atas OTP, tetapi tetap ditampilkan untuk tujuan edukatif dan sebagai *defense in depth* apabila kunci Vernam berkualitas lemah (mis. dibuat manual).

### Q16: Apa itu serangan Meet-in-the-Middle dan apakah mengancam skema Super Enkripsi kita?
**Jawaban:**
- **Definisi:** Serangan *Meet-in-the-Middle* (MitM) adalah serangan ruang-waktu (*time-space tradeoff*) terhadap enkripsi berganda di mana penyerang mengenkripsi plaintext dari sisi kiri dan mendekripsi ciphertext dari sisi kanan secara simultan, lalu mencari titik temu (*collision*) pada tabel penyimpanan perantara (seperti yang mereduksi keamanan Double-DES dari $2^{112}$ menjadi $2^{57}$).
- **Relevansi:** MitM membutuhkan pasangan plaintext-ciphertext yang diketahui dan memori sangat besar. Pada skema kami, ruang kunci total dipengaruhi kunci Vernam sepanjang pesan (kunci acak $\approx 5{,}95$ bit per byte), sehingga tabel perantara tidak layak dibuat untuk pesan yang cukup panjang. Namun ruang kunci lapisan klasik (Vigenère, Playfair) dan LFSR kecil secara terpisah memang kecil.

### Q17: Mengapa urutan dekripsi pada Super Enkripsi harus dibalik secara tepat (Vernam -> LFSR -> Vigenère -> Playfair)?
**Jawaban:**
Operasi enkripsi berantai merupakan komposisi fungsi matematika:
$$C_{\text{final}} = f_4(f_3(f_2(f_1(P))))$$
Berdasarkan sifat aljabar fungsi komposisi terbalikkan (*invertible composition*), invers dari komposisi fungsi adalah kebalikan dari urutan invers masing-masing fungsi:
$$(f_4 \circ f_3 \circ f_2 \circ f_1)^{-1} = f_1^{-1} \circ f_2^{-1} \circ f_3^{-1} \circ f_4^{-1}$$
Artinya, fungsi yang diterapkan terakhir ($f_4$ = Vernam) harus dibalik paling pertama ($f_4^{-1}$), diikuti $f_3^{-1}$ (LFSR), $f_2^{-1}$ (Vigenère), dan terakhir $f_1^{-1}$ (Playfair). Jika urutan ini diubah, data yang dihasilkan menjadi derau acak (*garbage data*) dan gagal dipulihkan. (Catatan: khusus untuk dua lapisan XOR, LFSR dan Vernam bersifat komutatif; urutan pada lapisan klasik tetap wajib dijaga.)

### Q18: Mengapa Playfair diletakkan di tahap pertama, bukan setelah Vigenère?
**Jawaban:**
Playfair menggabungkan huruf $J$ dan $I$ serta membuang karakter non-alfabet. Jika Playfair dijalankan setelah Vigenère, ciphertext Vigenère yang kebetulan mengandung huruf $J$ akan berubah menjadi $I$ sehingga tidak dapat dipulihkan dengan benar pada dekripsi (pesan yang dipulihkan rusak). Dengan Playfair di depan, kehilangan informasi hanya berupa sifat bawaan Playfair pada plaintext asli (spasi hilang, $J \rightarrow I$, padding `X`), dan semua tahap sesudahnya invertibel penuh.

### Q19: Mengapa hasil dekripsi Super Enkripsi tidak mengandung spasi dan ada huruf X tambahan?
**Jawaban:**
Itu sifat bawaan Playfair: spasi dan karakter non-huruf dibuang, $J$ digabung dengan $I$, huruf kembar disisipi `X`, dan panjang ganjil ditambah `X`. Ini bukan kesalahan dekripsi; tahap Vernam, LFSR, dan Vigenère memulihkan data secara persis. Contoh: `HELLO WORLD` menjadi `HELXLOWORLDX` setelah round-trip.
