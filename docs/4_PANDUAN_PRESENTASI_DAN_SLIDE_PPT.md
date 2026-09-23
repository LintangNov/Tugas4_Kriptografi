# Panduan Pembuatan Slide PPT dan Strategi Presentasi

Dokumen ini memandu tim dalam merancang berkas presentasi (PowerPoint / Canva / Google Slides) serta mengatur alur pembagian antara materi di slide dan materi saat demonstrasi aplikasi (*live demo*).

---

## 1. Prinsip Pemisahan: Slide PPT vs. Live Demo

Kesalahan paling umum dalam presentasi aplikasi kuliah adalah memasukkan tangkapan layar (*screenshot*) yang terlalu padat atau tabel berukuran besar ke dalam slide. Hal ini membuat slide terlihat membosankan (*slide clutter*) dan mengurangi antusiasme audiens terhadap demo langsung.

### Tabel Matriks Pembagian Konten:

| Topik / Komponen | Masukkan ke Slide PPT? | Tampilkan saat Live Demo? | Alasan & Strategi |
| :--- | :---: | :---: | :--- |
| **Identitas & Latar Belakang** | Ya | Tidak | Cukup disampaikan secara ringkas di slide pembuka. |
| **Peta Klasifikasi Algoritma** | Ya | Tidak | Gambaran perbandingan klasik vs modern (sandi substitusi vs sandi aliran) lebih mudah dipahami dalam bentuk diagram taksonomi di slide. |
| **Formulasi Matematika Inti** | Ya | Tidak | Tampilkan rumus formal ($C_i = (P+K) \bmod 26$, $C_i = P_i \oplus K_i$) di slide untuk menunjukkan landasan teori yang kuat. |
| **Tabel Pergeseran Vigenère Penuh** | Tidak | Ya | Jangan menaruh tabel puluhan baris di slide. Tunjukkan interaktivitas tabel di aplikasi saat memasukkan teks uji. |
| **Grid Matriks 5x5 Playfair** | Ya (Prinsipnya saja) | Ya (Interaksi Sel) | Di slide cukup tampilkan contoh aturan Baris/Kolom/Persegi. Di demo, operasikan fitur dropdown penyorotan sel kuning/hijau. |
| **Tabel XOR Biner Vernam (per byte)** | Tidak (cukup 1 contoh kecil) | Ya | Di slide cukup satu contoh 1-2 karakter. Saat demo, tunjukkan tabel biner P, K, dan hasil XOR untuk seluruh pesan. |
| **Jejak Clock Register LFSR** | Ya (Diagram register + polinomial) | Ya (Tabel Clock) | Gambar register 4 bit dengan tap di slide. Saat demo, tunjukkan tabel state, feedback, dan bit output serta variasikan seed dan ukuran register. |
| **Pipeline Super Enkripsi** | Ya (Diagram Alur Blok) | Ya (Eksekusi 4 Layer + Simpan Kunci Vernam) | Tampilkan arsitektur aliran data di slide, lalu tunjukkan eksekusi bertingkat dan diagram Graphviz langsung di aplikasi. |
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
  - Kurangnya visualisasi transparan pada tahapan internal algoritma (seperti XOR biner per bit atau pergeseran state register LFSR).
  - Kebutuhan akan platform komputasi edukatif yang memadukan sandi klasik (substitusi alfabetik) dan modern (sandi aliran).
- **Catatan Pembicara:** Jelaskan bahwa proyek ini bertujuan membangun platform *white-box* interaktif agar mekanisme matematis setiap algoritma dapat diamati secara riil.

### Slide 3: Taksonomi Algoritma yang Dikembangkan
- **Diagram/Tabel Sederhana:**
  - **Kriptografi Klasik:**
    - Vigenère Cipher (Polialfabetik)
    - Playfair Cipher (Substitusi Bigram, Matriks $5 \times 5$)
  - **Kriptografi Modern (Sandi Aliran / Stream Cipher):**
    - Vernam Cipher / One-Time Pad (XOR dengan kunci acak sepanjang pesan)
    - LFSR-based Stream Cipher (keystream dari Linear Feedback Shift Register)
  - **Kombinasi (Hybrid):**
    - Super Enkripsi (Pipa Berurutan 4 Tahap: Playfair, Vigenère, LFSR, Vernam)

### Slide 4: Landasan Matematis - Vigenère & Playfair
- **Vigenère:**
  $$C_i = (P_i + K_i) \pmod{26}, \quad P_i = (C_i - K_i + 26) \pmod{26}$$
- **Playfair:**
  - Peleburan $J \rightarrow I$, penanganan huruf kembar via penyisipan $X$.
  - 3 Aturan Geometri: Baris Sama (geser horizontal), Kolom Sama (geser vertikal), Persegi Panjang (tukar kolom).
- **Catatan Pembicara:** Tekankan bahwa Playfair adalah langkah awal historis untuk mematahkan analisis frekuensi huruf tunggal dengan mengoperasikan pasangan huruf (*digraph*).

### Slide 5: Landasan Matematis - Vernam Cipher (One-Time Pad)
- **Rumus:**
  $$C_i = P_i \oplus K_i, \quad P_i = C_i \oplus K_i$$
- **Syarat OTP (Perfect Secrecy, Shannon):**
  - Kunci acak sejati.
  - Panjang kunci = panjang pesan.
  - Kunci hanya dipakai sekali.
- **Contoh Singkat:** `H` (01001000) $\oplus$ `X` (01011000) = 00010000 = `10`.
- **Catatan Pembicara:** Jelaskan bahwa XOR adalah invers dirinya sendiri sehingga enkripsi dan dekripsi memakai operasi yang sama, dan sebutkan bahaya *two-time pad* ($C_1 \oplus C_2 = P_1 \oplus P_2$).

### Slide 6: Landasan Matematis - LFSR Stream Cipher
- **Prinsip:** Seed pendek diperluas menjadi keystream pseudo-acak oleh register geser dengan umpan balik XOR.
- **Diagram Register 4 bit:** polinomial $x^4 + x^3 + 1$, tap 4 dan 3, output bit paling kanan, periode maksimum $2^4 - 1 = 15$.
- **Operasi:** $C_i = P_i \oplus KS_i$ (8 clock per byte keystream).
- **Catatan Pembicara:** Tegaskan bahwa LFSR tunggal bersifat linear sehingga dapat dipecahkan dengan Berlekamp-Massey; sistem nyata memakai kombinasi non-linear. Implementasi ini untuk tujuan edukatif.

### Slide 7: Arsitektur Super Enkripsi (Hybrid Pipeline)
- **Diagram Blok:**
  $$\text{Plaintext} \xrightarrow{\text{Playfair}} C_1 \xrightarrow{\text{Vigenère}} C_2 \xrightarrow{\text{LFSR}} C_3 \text{ (byte)} \xrightarrow{\text{Vernam}} C_{\text{final}} \text{ (Hex)}$$
- **Prinsip Dekripsi Terbalik:**
  $$(f_4 \circ f_3 \circ f_2 \circ f_1)^{-1} = f_1^{-1} \circ f_2^{-1} \circ f_3^{-1} \circ f_4^{-1}$$
- **Normalisasi Data:** Menjelaskan bahwa data biner hasil LFSR/Vernam ditampilkan sebagai heksadesimal, dan alasan Playfair diletakkan di tahap pertama (menghindari kerusakan $J \rightarrow I$ pada ciphertext Vigenère).

### Slide 8: Transisi ke Live Demo (Intermission Slide)
- **Teks Utama:** "Demonstrasi Langsung Aplikasi Web (Streamlit)"
- **Daftar Skenario Pengujian yang Akan Didemokan:**
  1. Pengujian Vigenère dengan kunci periodik.
  2. Pengujian Playfair dengan kata kunci dan inspeksi sel matriks.
  3. Pengujian Vernam dengan kunci acak otomatis (tabel XOR biner).
  4. Pengujian LFSR dengan variasi seed dan ukuran register (jejak clock).
  5. Pengujian Super Enkripsi end-to-end (Enkripsi berlapis dan pemulihan kembali).
- **Catatan Pembicara:** Beralih layar dari slide PPT ke jendela browser.

### Slide 9: Analisis Keamanan & Diskusi Komparatif
- **Perbandingan Efisiensi & Kekuatan:**
  - Sandi klasik (Vigenère/Playfair) rentan terhadap analisis frekuensi dan pencarian kunci otomatis (*brute force* ruang kunci kecil).
  - Vernam/OTP menyediakan *perfect secrecy* secara teoretis, tetapi menuntut kunci sepanjang pesan yang acak dan sekali pakai (distribusi kunci sulit).
  - LFSR praktis (seed pendek) namun linear sehingga rentan terhadap Berlekamp-Massey jika berdiri sendiri.
  - Super Enkripsi memadukan seluruh lapisan dengan prinsip *Defense in Depth*; dua lapisan XOR (LFSR dan Vernam) secara matematis setara satu sandi aliran, dengan kekuatan ditentukan kunci Vernam.

### Slide 10: Kesimpulan & Penutup
- **Kesimpulan:**
  - Aplikasi berhasil memvisualisasikan seluruh tahapan algoritma secara transparan dan deterministik.
  - Aliran data pada Super Enkripsi terbukti *invertible* (dengan catatan sifat bawaan Playfair: spasi hilang, $J \rightarrow I$, padding `X`).
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
   - *Kunci Vernam:* aktifkan opsi acak otomatis (salin kunci yang tampil untuk dekripsi)
   - *LFSR:* register 8 bit, seed `10110001` (untuk contoh manual: register 4 bit, seed `1001`)
3. **Sorot Fitur Unggulan:**
   - Saat mendemokan Playfair, luangkan 30 detik untuk mendemonstrasikan **dropdown inspeksi digraph**, tunjukkan bagaimana sel matriks berubah warna (kuning untuk input, hijau untuk output). Dosen sangat mengapresiasi visualisasi yang interaktif.
   - Saat mendemokan Vernam, tunjukkan tabel biner P, K, dan hasil XOR, lalu dekripsi dengan kunci yang sama. Coba ubah 1 karakter kunci untuk menunjukkan hasil dekripsi menjadi salah.
   - Saat mendemokan LFSR, pilih register 4 bit, seed `1001`, dan tunjukkan tabel jejak clock (cocok dengan hitungan manual di dokumen 1). Lalu ubah seed dan tunjukkan ciphertext berubah total.
   - Saat mendemokan Super Enkripsi, klik proses enkripsi, **salin ciphertext final dan kunci Vernam** ke tab dekripsi, dan tunjukkan bahwa plaintext pulih (tanpa spasi dan dengan padding `X` karena sifat Playfair).
