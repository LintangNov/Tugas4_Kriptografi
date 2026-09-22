# Panduan Pembuatan Slide PPT dan Strategi Presentasi

Dokumen ini memandu tim dalam merancang berkas presentasi (PowerPoint / Canva / Google Slides) serta mengatur alur pembagian antara materi di slide dan materi saat demonstrasi aplikasi (*live demo*).

---

## 1. Prinsip Pemisahan: Slide PPT vs. Live Demo

Kesalahan paling umum dalam presentasi aplikasi kuliah adalah memasukkan tangkapan layar (*screenshot*) yang terlalu padat atau tabel berukuran besar ke dalam slide. Hal ini membuat slide terlihat membosankan (*slide clutter*) dan mengurangi antusiasme audiens terhadap demo langsung.

### Tabel Matriks Pembagian Konten:

| Topik / Komponen | Masukkan ke Slide PPT? | Tampilkan saat Live Demo? | Alasan & Strategi |
| :--- | :---: | :---: | :--- |
| **Identitas & Latar Belakang** | Ya | Tidak | Cukup disampaikan secara ringkas di slide pembuka. |
| **Peta Klasifikasi Algoritma** | Ya | Tidak | Gambaran perbandingan klasik vs modern, simetris vs asimetris lebih mudah dipahami dalam bentuk diagram taksonomi di slide. |
| **Formulasi Matematika Inti** | Ya | Tidak | Tampilkan rumus formal ($C_i = (P+K) \bmod 26$, $C = M^e \bmod n$) di slide untuk menunjukkan landasan teori yang kuat. |
| **Tabel Pergeseran Vigenère Penuh** | Tidak | Ya | Jangan menaruh tabel puluhan baris di slide. Tunjukkan interaktivitas tabel di aplikasi saat memasukkan teks uji. |
| **Grid Matriks 5x5 Playfair** | Ya (Prinsipnya saja) | Ya (Interaksi Sel) | Di slide cukup tampilkan contoh aturan Baris/Kolom/Persegi. Di demo, operasikan fitur dropdown penyorotan sel kuning/hijau. |
| **Tabel Lengkap S-Box & 11 Round Key AES** | Tidak | Ya | Sangat membuang ruang slide. Cukup jelaskan konsep SPN di slide, lalu buka expander 11 Round Key di aplikasi saat demo. |
| **State Matrix 4x4 AES (SubBytes dll.)** | Konsep Saja | Ya (Tabel Hex) | Jelaskan di slide bahwa ada 4 tahap. Tunjukkan perubahan angka heksadesimalnya langsung di web. |
| **Penghitungan Nilai e & d RSA** | Ya (Ringkasan Rumus) | Ya (Input Prima) | Tampilkan rumus Extended Euclidean di slide. Saat demo, variasikan nilai prima $p$ dan $q$ untuk menunjukkan responsivitas sistem. |
| **Pipeline Super Enkripsi** | Ya (Diagram Alur Blok) | Ya (Eksekusi 4 Layer) | Tampilkan arsitektur aliran data di slide, lalu tunjukkan eksekusi bertingkat dan diagram Graphviz langsung di aplikasi. |
| **Analisis Keamanan & Kesimpulan** | Ya | Tidak | Poin-poin kesimpulan dan rekomendasi akademis wajib dirangkum di slide penutup. |

---

## 2. Struktur Rinci Slide PPT (Rekomendasi 10 - 12 Slide)

### Slide 1: Judul & Identitas
- **Judul:** Sistem Kriptografi Terpadu: Implementasi dan Visualisasi Algoritma Klasik, Modern, dan Super Enkripsi
- **Sub-judul:** Tugas Besar Mata Kuliah Kriptografi - Semester 5
- **Konten:** Nama Anggota Kelompok, NIM, Program Studi, Fakultas, Universitas, dan Tahun Ajaran.
- **Catatan Pembicara:** Ucapkan salam pembuka formal, perkenalkan diri dan anggota tim secara singkat, lalu sampaikan tujuan presentasi.

### Slide 2: Latar Belakang & Masalah
- **Poin Utama:**
  - Kriptografi sering kali dipelajari sebatas rumus abstrak di atas kertas (*black-box concept*).
  - Kurangnya visualisasi transparan pada tahapan internal algoritma (seperti pergeseran state AES atau invers modular RSA).
  - Kebutuhan akan platform komputasi edukatif yang memadukan sandi klasik (substitusi alfabetik) dan modern (blok simetris & kunci publik).
- **Catatan Pembicara:** Jelaskan bahwa proyek ini bertujuan membangun platform *white-box* interaktif agar mekanisme matematis setiap algoritma dapat diamati secara riil.

### Slide 3: Taksonomi Algoritma yang Dikembangkan
- **Diagram/Tabel Sederhana:**
  - **Kriptografi Klasik:**
    - Vigenère Cipher (Polialfabetik)
    - Playfair Cipher (Substitusi Bigram, Matriks $5 \times 5$)
  - **Kriptografi Modern:**
    - AES-128 (Sandi Blok Simetris, Standar FIPS PUB 197)
    - RSA (Sandi Asimetris Kunci Publik, Berbasis Faktorisasi Prima)
  - **Kombinasi (Hybrid):**
    - Super Enkripsi (Pipa Berurutan 4 Tahap)

### Slide 4: Landasan Matematis - Vigenère & Playfair
- **Vigenère:**
  $$C_i = (P_i + K_i) \pmod{26}, \quad P_i = (C_i - K_i + 26) \pmod{26}$$
- **Playfair:**
  - Peleburan $J \rightarrow I$, penanganan huruf kembar via penyisipan $X$.
  - 3 Aturan Geometri: Baris Sama (geser horizontal), Kolom Sama (geser vertikal), Persegi Panjang (tukar kolom).
- **Catatan Pembicara:** Tekankan bahwa Playfair adalah langkah awal historis untuk mematahkan analisis frekuensi huruf tunggal dengan mengoperasikan pasangan huruf (*digraph*).

### Slide 5: Landasan Matematis - AES-128
- **Karakteristik Utama:** Blok 128-bit, Kunci 128-bit, 10 Putaran (*Rounds*).
- **Struktur Putaran (SPN):**
  - `SubBytes` (S-Box) $\rightarrow$ Konfusi Non-Linear.
  - `ShiftRows` $\rightarrow$ Difusi Baris.
  - `MixColumns` $\rightarrow$ Difusi Kolom dalam Medan Galois $GF(2^8)$.
  - `AddRoundKey` $\rightarrow$ Injeksi Kunci Rahasia.
- **Catatan Pembicara:** Sebutkan bahwa pada Round 10 MixColumns dihilangkan demi simetri arsitektur enkripsi-dekripsi tanpa mengorbankan keamanan.

### Slide 6: Landasan Matematis - RSA
- **Dasar Teori:** Teorema Euler dan Masalah Faktorisasi Prima (*Integer Factorization Problem*).
- **Alur Kunci:**
  - $n = p \times q$, $\quad \phi(n) = (p-1)(q-1)$.
  - $\gcd(e, \phi(n)) = 1$.
  - Invers Modular: $e \cdot d \equiv 1 \pmod{\phi(n)}$ (Extended Euclidean Algorithm).
- **Operasi:**
  - Enkripsi: $C = M^e \pmod n$.
  - Dekripsi: $M = C^d \pmod n$.
- **Catatan Pembicara:** Tegaskan bahwa implementasi ini menggunakan prima kecil untuk demonstrasi transparan per karakter, dan sebutkan standar produksi adalah $\ge 2048$ bit.

### Slide 7: Arsitektur Super Enkripsi (Hybrid Pipeline)
- **Diagram Blok:**
  $$\text{Plaintext} \xrightarrow{\text{Vigenère}} C_1 \xrightarrow{\text{Playfair}} C_2 \xrightarrow{\text{AES-128}} C_3 \text{ (Base64)} \xrightarrow{\text{RSA}} C_{\text{final}} \text{ (Integers)}$$
- **Prinsip Dekripsi Terbalik:**
  $$(f_4 \circ f_3 \circ f_2 \circ f_1)^{-1} = f_1^{-1} \circ f_2^{-1} \circ f_3^{-1} \circ f_4^{-1}$$
- **Normalisasi Data:** Menjelaskan peran Base64 sebagai jembatan antara keluaran biner AES dan masukan numerik RSA.

### Slide 8: Transisi ke Live Demo (Intermission Slide)
- **Teks Utama:** "Demonstrasi Langsung Aplikasi Web (Streamlit)"
- **Daftar Skenario Pengujian yang Akan Didemokan:**
  1. Pengujian Vigenère dengan kunci periodik.
  2. Pengujian Playfair dengan kata kunci dan inspeksi sel matriks.
  3. Pengujian AES pada blok pertama (Padding dan State Matrix $4 \times 4$).
  4. Pengujian RSA dengan pemilihan prima interaktif.
  5. Pengujian Super Enkripsi end-to-end (Enkripsi berlapis dan pemulihan kembali).
- **Catatan Pembicara:** Beralih layar dari slide PPT ke jendela browser.

### Slide 9: Analisis Keamanan & Diskusi Komparatif
- **Perbandingan Efisiensi & Kekuatan:**
  - Sandi klasik (Vigenère/Playfair) rentan terhadap analisis frekuensi dan pencarian kunci otomatis (*brute force* ruang kunci kecil).
  - AES-128 menyediakan keamanan komputasi simetris terbaik untuk data berukuran besar.
  - RSA memberikan mekanisme distribusi kunci tanpa memerlukan saluran rahasia bersama (*shared secret*).
  - Super Enkripsi memadukan seluruh keunggulan di atas dengan prinsip *Defense in Depth*.

### Slide 10: Kesimpulan & Penutup
- **Kesimpulan:**
  - Aplikasi berhasil memvisualisasikan seluruh tahapan algoritma secara transparan dan deterministik.
  - Aliran data pada Super Enkripsi terbukti *invertible* tanpa kehilangan integritas data.
- **Sesi Tanya Jawab:** "Terima kasih. Kami mengundang Bapak/Ibu Dosen dan rekan-rekan untuk memberikan pertanyaan dan tanggapan."

---

## 3. Rundown & Manajemen Waktu Presentasi (Total 20 Menit)

| Waktu | Durasi | Agenda / Aktivitas | Penanggung Jawab |
| :---: | :---: | :--- | :--- |
| **00:00 - 02:00** | 2 Menit | Pembukaan, Latar Belakang, & Pembagian Materi | Anggota 1 |
| **02:00 - 06:00** | 4 Menit | Pembahasan Teori Inti (Slide 3 s/d 7) | Anggota 1 & 2 |
| **06:00 - 13:00** | 7 Menit | **Live Demo Aplikasi Web di Browser** | Anggota 2 & 3 |
| **13:00 - 15:00** | 2 Menit | Analisis Keamanan, Evaluasi, & Kesimpulan (Slide 9-10) | Anggota 3 |
| **15:00 - 20:00** | 5 Menit | **Sesi Tanya Jawab Dosen (Q&A Defense)** | Seluruh Anggota Tim |

---

## 4. Tips Teknis Menjalankan Live Demo

1. **Persiapan Browser:**
   - Jalankan `streamlit run app.py` sebelum giliran presentasi dimulai, pastikan server sudah berjalan di `http://localhost:8501`.
   - Buka browser dalam kondisi layar penuh (*Full Screen* / F11) agar tampilan bersih dari bookmark dan tab lain.
2. **Siapkan Teks Pengujian (Cheat Sheet Data):**
   Siapkan teks sampel standar di notepad agar saat demo tidak perlu mengetik panjang atau bingung memikirkan kata:
   - *Plaintext sampel:* `KRIPTOGRAFI EDISI SEMESTER LIMA`
   - *Kunci Vigenère:* `KUNCI`
   - *Kunci Playfair:* `MONARCHY`
   - *Kunci AES:* `KunciRahasia1234`
   - *Prima RSA:* $p = 61, q = 53, e = 17$
3. **Sorot Fitur Unggulan:**
   - Saat mendemokan Playfair, luangkan 30 detik untuk mendemonstrasikan **dropdown inspeksi digraph**, tunjukkan bagaimana sel matriks berubah warna (kuning untuk input, hijau untuk output). Dosen sangat mengapresiasi visualisasi yang interaktif.
   - Saat mendemokan AES, tunjukkan **expander Pre-Round dan Round 1**, jelaskan bagaimana nilai heksadesimal berubah dari SubBytes ke ShiftRows.
   - Saat mendemokan Super Enkripsi, klik proses enkripsi, lalu salin ciphertext final ke tab dekripsi, dan tunjukkan bahwa plaintext berhasil pulih 100%.
