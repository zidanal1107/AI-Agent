# Panduan Alur Kerja Program

## Tujuan program

Program ini membantu pengguna membuat folder, membuat file, dan mengisi file dengan bantuan Ollama. Ollama adalah program AI yang berjalan di komputer sendiri. AI akan menerima perintah dalam bahasa biasa, lalu menuliskan isi file sesuai perintah tersebut.

Contohnya, pengguna dapat meminta: “Buat halaman web sederhana untuk menampilkan daftar belanja.” Jika file yang dipilih adalah `belanja.html`, AI akan membuat isi file HTML untuk kebutuhan tersebut.

## Yang perlu disiapkan

Sebelum memakai fitur AI, pastikan dua hal berikut sudah tersedia.

1. Python 3 terpasang di komputer.
2. Ollama sudah terpasang, sedang berjalan, dan memiliki model `qwen2.5:3b`.

Untuk menyiapkan model, jalankan perintah ini sekali di terminal:

```bash
ollama pull qwen2.5:3b
```

Jika layanan Ollama belum berjalan, buka terminal lain lalu jalankan:

```bash
ollama serve
```

## Cara menjalankan program

1. Buka terminal di folder `V2`.
2. Jalankan perintah berikut:

   ```bash
   python main.py
   ```

3. Program akan menampilkan tiga pilihan:

   ```text
   1. Buat folder
   2. Buat file
   3. Isi file
   ```

4. Ketik angka pilihan, lalu tekan Enter.

Semua folder dan file yang dibuat program berada di dalam folder `workspace`. Program menolak lokasi yang mencoba keluar dari folder tersebut, sehingga area kerja tetap rapi dan lebih aman.

## Alur kerja utama

```text
Mulai program
      ↓
Pilih tindakan: buat folder, buat file, atau isi file
      ↓
Masukkan lokasi file/folder di dalam workspace
      ↓
Jika memilih “Isi file”, tulis perintah untuk AI
      ↓
Ollama membuat isi file sesuai perintah
      ↓
Program menyimpan hasil ke file yang dipilih
```

## Penjelasan setiap pilihan

### 1. Buat folder

Pilih `1` jika ingin membuat tempat penyimpanan baru. Masukkan nama folder atau lokasi folder relatif dari `workspace`.

Contoh input:

```text
project_web/gambar
```

Hasilnya, program membuat folder `workspace/project_web/gambar`. Jika folder `project_web` belum ada, program juga akan membuatnya.

### 2. Buat file

Pilih `2` jika ingin membuat file kosong. Masukkan nama dan lokasi file relatif dari `workspace`.

Contoh input:

```text
project_web/index.html
```

Program membuat file `index.html` di dalam folder `workspace/project_web`. File yang sudah ada tidak akan ditimpa oleh pilihan ini.

### 3. Isi file dengan Ollama

Pilih `3` jika ingin AI mengisi sebuah file. Alurnya sebagai berikut:

1. Program menampilkan daftar folder dan file di `workspace`.
2. Masukkan file yang ingin diisi, misalnya `project_web/index.html`.
3. Program menampilkan jenis file, misalnya `.html`, `.py`, atau `.js`.
4. Tulis perintah yang menjelaskan hasil yang diinginkan.
5. Program mengirim perintah tersebut, jenis file, dan isi file sebelumnya ke Ollama.
6. Ollama mengembalikan isi file baru, lalu program menyimpannya.

Contoh penggunaan untuk file Python:

```text
File yang ingin diisi: latihan/sapaan.py
Tipe file yang dipilih: .py
Perintah untuk Ollama: Buat program yang meminta nama pengguna lalu menyapa dengan ramah.
```

Contoh penggunaan untuk file JavaScript:

```text
File yang ingin diisi: web/tombol.js
Tipe file yang dipilih: .js
Perintah untuk Ollama: Buat tombol yang menampilkan pesan “Selamat datang” saat diklik.
```

## Hal penting sebelum menyimpan

Fitur isi file mengganti seluruh isi file dengan jawaban dari AI. Isi lama memang dikirim sebagai konteks agar AI dapat menyesuaikan hasilnya, tetapi hasil AI tetap perlu diperiksa sebelum dipakai.

Sebelum memberi perintah, sebaiknya:

- Pastikan file yang dipilih benar.
- Simpan salinan file penting terlebih dahulu.
- Jelaskan permintaan secara spesifik, misalnya sebutkan fungsi, tampilan, atau bahasa yang diinginkan.
- Baca hasil AI dan coba jalankan programnya sebelum digunakan lebih lanjut.

## Jika terjadi masalah

| Pesan atau kondisi | Arti dan tindakan |
| --- | --- |
| `File tidak ditemukan` | Periksa kembali nama dan lokasi file. Buat file terlebih dahulu melalui pilihan 2 bila belum ada. |
| `Path tidak valid` | Gunakan lokasi di dalam `workspace`; jangan memakai `..` atau alamat lengkap komputer. |
| `Tidak dapat terhubung ke Ollama` | Pastikan Ollama sedang berjalan dengan `ollama serve`. |
| Model belum tersedia | Jalankan `ollama pull qwen2.5:3b`. |
| Hasil AI tidak sesuai | Perjelas perintah, lalu jalankan menu 3 lagi. |

## Ringkasan

Program ini memberikan alur sederhana: buat tempat kerja, buat file, lalu minta AI mengisi file sesuai kebutuhan. Pengguna tidak perlu menulis kode dari awal, tetapi tetap perlu memeriksa hasil AI agar sesuai dengan tujuan dan aman digunakan.
