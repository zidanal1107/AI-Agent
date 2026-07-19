# Laporan Review Kode — V2

Tanggal review: 19 Juli 2026  
Ruang lingkup: `main.py` dan `llm/llm.py`

## Ringkasan

Program sudah memiliki alur dasar untuk memilih aksi dan membuat folder/file. Namun, dalam kondisi saat ini aplikasi belum bisa dijalankan karena dependensi `requests` belum tersedia. Selain itu, ada fitur yang ditampilkan tetapi belum diimplementasikan, serta beberapa risiko kehilangan data dan akses path di luar `workspace`.

## Temuan prioritas tinggi

### 1. Aplikasi gagal mulai bila `requests` belum terpasang

**Lokasi:** `main.py:1`, `llm/llm.py:1`  
**Dampak:** Saat menjalankan `python main.py`, program langsung berhenti dengan `ModuleNotFoundError: No module named 'requests'`. Ini terjadi walaupun fitur LLM belum digunakan, karena modul LLM selalu diimpor di awal.

**Saran perbaikan:**

- Tambahkan daftar dependensi, misalnya `requirements.txt` berisi `requests`.
- Atau, impor `llm` hanya saat fitur LLM benar-benar dipakai.
- Tampilkan pesan instalasi yang jelas bila dependensi belum ada.

### 2. Pilihan “Isi file” belum diimplementasikan

**Lokasi:** `main.py:24`, menu utama  
**Dampak:** Menu menampilkan tiga pilihan, tetapi hanya kondisi `goal == 1` dan `goal == 2` yang tersedia. Jika pengguna memilih `3`, program selesai tanpa melakukan apa pun dan tanpa penjelasan.

**Saran perbaikan:** Tambahkan blok `elif goal == 3` untuk meminta lokasi file serta isi baru, lalu simpan dengan validasi yang aman. Bila fitur belum siap, hapus pilihan tersebut dari menu.

### 3. Pembuatan file dapat menimpa file yang sudah ada tanpa peringatan

**Lokasi:** `main.py:63`  
**Dampak:** File dibuka dengan mode `"w"`, yang akan mengosongkan dan menulis ulang file yang sudah ada. Blok `except FileExistsError` tidak akan terpanggil pada mode ini, sehingga pengguna bisa kehilangan isi file.

**Saran perbaikan:** Gunakan mode `"x"` untuk hanya membuat file baru, atau cek keberadaan file terlebih dahulu lalu minta konfirmasi eksplisit sebelum menimpa.

### 4. Input lokasi dapat keluar dari folder `workspace`

**Lokasi:** `main.py:44`, `main.py:63`  
**Dampak:** Nilai seperti `../../folder_lain` dapat membuat atau menulis file di luar `workspace`. Ini berisiko, terutama jika aplikasi menerima input dari pengguna lain.

**Saran perbaikan:** Bangun path memakai `pathlib.Path`, normalisasi dengan `resolve()`, lalu pastikan path hasilnya tetap berada di bawah direktori `workspace` sebelum melakukan operasi file.

## Temuan prioritas menengah

### 5. `workspace` harus sudah ada agar menu folder/file bisa dipakai

**Lokasi:** `main.py:28`, `main.py:51`  
**Dampak:** Fungsi `tree("workspace")` akan gagal bila folder tersebut belum ada. Pada salinan kerja saat review, folder `workspace` memang tidak tersedia, sehingga alur menu tidak dapat dilanjutkan.

**Saran perbaikan:** Definisikan lokasi workspace relatif terhadap file program, kemudian buat otomatis dengan `workspace.mkdir(parents=True, exist_ok=True)` sebelum memanggil `tree` atau menulis data.

### 6. Fungsi LLM belum tahan terhadap kegagalan layanan

**Lokasi:** `llm/llm.py:3`  
**Dampak:** Jika Ollama tidak berjalan, respons bukan JSON, server mengembalikan error, atau koneksi macet, fungsi dapat melempar exception yang tidak jelas dan berpotensi menunggu tanpa batas karena tidak ada `timeout`.

**Saran perbaikan:** Tambahkan `timeout`, panggil `response.raise_for_status()`, tangani `requests.RequestException` dan kesalahan JSON, serta beri pesan yang menjelaskan bahwa layanan Ollama/model perlu dijalankan.

### 7. Validasi input kurang fleksibel dan memakai `except` terlalu umum

**Lokasi:** `main.py:36-40`, `main.py:54-58`  
**Dampak:** Input dipisah dengan `split()` dan hanya mengambil dua token pertama. Nama/lokasi yang mengandung spasi tidak didukung; token tambahan diam-diam diabaikan. `except:` juga dapat menyembunyikan kesalahan pemrograman yang tidak terkait format input.

**Saran perbaikan:** Validasi jumlah token secara eksplisit atau gunakan format input yang lebih jelas. Tangkap exception spesifik seperti `IndexError` atau, lebih baik, hindari exception untuk alur validasi normal.

### 8. Tampilan tree belum menangani error dan struktur cabang kurang akurat

**Lokasi:** `main.py:6-16`  
**Dampak:** Folder yang tidak dapat dibaca atau tidak ada akan menghentikan program. Indentasi semua cabang juga selalu memakai `│`, sehingga struktur pohon bisa membingungkan untuk folder dengan banyak item.

**Saran perbaikan:** Tangani `FileNotFoundError` dan `PermissionError`; gunakan informasi item terakhir untuk memilih konektor `└──` atau `├──`.

## Peningkatan kualitas kode

- Gunakan `Path` secara konsisten; saat ini `pathlib.Path` baru dipakai di fungsi `tree`, sedangkan operasi lain masih merangkai string path.
- Hapus impor `from llm.llm import llm` sampai fitur dipakai, atau aktifkan fitur LLM secara lengkap. Saat ini baris penggunaan LLM masih dikomentari.
- Tambahkan `README.md` berisi cara instalasi, kebutuhan Ollama/model `qwen2.5:3b`, dan contoh format input.
- Tambahkan pengujian sederhana untuk: input menu tidak valid, workspace belum ada, pembuatan folder/file, file yang sudah ada, dan percobaan path traversal.

## Verifikasi yang dilakukan

- Sintaks `main.py` dan `llm/llm.py` lolos pemeriksaan `py_compile`.
- Menjalankan `python main.py` gagal pada impor `requests` yang belum tersedia.
- Tidak ditemukan berkas manifest dependensi (`requirements.txt` atau `pyproject.toml`) di folder `V2`.

## Kesimpulan

Struktur awalnya sudah cocok untuk latihan pengelolaan folder dan file, tetapi belum siap dipakai dengan aman. Prioritas perbaikan: perbaiki dependensi/impor LLM, implementasikan atau hapus menu nomor 3, cegah penimpaan file, dan batasi semua path agar tetap di dalam `workspace`.
