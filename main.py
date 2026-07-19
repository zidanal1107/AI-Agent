from pathlib import Path

from llm.llm import llm


WORKSPACE = Path(__file__).parent / "workspace"


def tree(path: Path, prefix: str = "") -> None:
    """Tampilkan isi folder secara sederhana."""
    print(f"{prefix}{path.name}")

    for item in sorted(path.iterdir(), key=lambda entry: (entry.is_file(), entry.name.lower())):
        if item.is_dir():
            tree(item, prefix + "│   ")
        else:
            print(f"{prefix}│   {item.name}")


def path_di_workspace(path_input: str) -> Path | None:
    """Ubah path relatif menjadi path aman di dalam workspace."""
    kandidat = Path(path_input.strip())

    if not path_input.strip() or kandidat.is_absolute() or ".." in kandidat.parts:
        return None

    path_final = (WORKSPACE / kandidat).resolve()
    try:
        path_final.relative_to(WORKSPACE.resolve())
    except ValueError:
        return None
    return path_final


def pilih_goal() -> int:
    while True:
        pilihan = input("Pilih goal (1-3): ").strip()
        if pilihan in {"1", "2", "3"}:
            return int(pilihan)
        print("Masukkan angka 1, 2, atau 3.")


def buat_folder() -> None:
    tree(WORKSPACE)
    path = path_di_workspace(input("Nama/lokasi folder relatif dari workspace: "))
    if path is None:
        print("Path tidak valid. Gunakan path relatif dan jangan gunakan '..'.")
        return

    try:
        path.mkdir(parents=True)
        print(f"Folder berhasil dibuat: {path.relative_to(WORKSPACE)}")
    except FileExistsError:
        print("Folder sudah ada.")
    except OSError as error:
        print(f"Gagal membuat folder: {error}")


def buat_file() -> None:
    tree(WORKSPACE)
    path = path_di_workspace(input("Nama/lokasi file relatif dari workspace: "))
    if path is None:
        print("Path tidak valid. Gunakan path relatif dan jangan gunakan '..'.")
        return
    if path == WORKSPACE.resolve():
        print("Masukkan nama file yang valid.")
        return

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=False)
        print(f"File berhasil dibuat: {path.relative_to(WORKSPACE)}")
    except FileExistsError:
        print("File sudah ada.")
    except OSError as error:
        print(f"Gagal membuat file: {error}")


def isi_file() -> None:
    tree(WORKSPACE)
    path = path_di_workspace(input("File yang ingin diisi (relatif dari workspace): "))
    if path is None or not path.is_file():
        print("File tidak ditemukan atau path tidak valid.")
        return

    ekstensi = path.suffix or "tanpa ekstensi"
    print(f"Tipe file yang dipilih: {ekstensi}")
    perintah = input("Perintah untuk Ollama (isi file yang diinginkan): ").strip()
    if not perintah:
        print("Perintah tidak boleh kosong.")
        return

    try:
        isi_lama = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("File bukan teks UTF-8 sehingga tidak dapat diisi oleh Ollama.")
        return
    except OSError as error:
        print(f"Gagal membaca file: {error}")
        return

    prompt = f"""Kamu adalah pembuat kode. Isi seluruh file berikut sesuai perintah pengguna.
Nama file: {path.name}
Ekstensi/tipe file: {ekstensi}
Perintah pengguna: {perintah}

Isi file saat ini:
---
{isi_lama}
---

Balas HANYA dengan isi akhir file. Jangan gunakan markdown, blok kode, penjelasan, atau kata pembuka."""

    print("Ollama sedang membuat isi file...")
    try:
        isi_baru = llm(prompt)
    except (RuntimeError, ValueError) as error:
        print(f"Gagal meminta Ollama: {error}")
        return

    try:
        path.write_text(isi_baru, encoding="utf-8")
        print(f"Isi file berhasil disimpan: {path.relative_to(WORKSPACE)}")
    except OSError as error:
        print(f"Gagal menyimpan file: {error}")


def main() -> None:
    WORKSPACE.mkdir(exist_ok=True)
    print("=== PILIHAN GOAL ===")
    print("1. Buat folder\n2. Buat file\n3. Isi file")

    goal = pilih_goal()
    if goal == 1:
        buat_folder()
    elif goal == 2:
        buat_file()
    else:
        isi_file()


if __name__ == "__main__":
    main()
