from llm.llm import llm
import os
from pathlib import Path

def tree(path, prefix=""):
    path = Path(path)

    print(prefix + path.name)

    for item in path.iterdir():
        if item.is_dir():
            tree(item, prefix + "│   ")
        else:
            print(prefix + "│   " + item.name)

def main():
    print("=== PILIHAN GOAL ===")
    print("1. Buat folder\n2. Buat file\n3. Isi file")

    while True:
        goal = input("Pilih goal: ")

        if goal.isdigit():
            goal = int(goal)

            if goal > 3 or goal < 1:
                print("Pilih goal anda sesuai dengan pilihan (1-3)")
            else:
                break
        else:
            print("Pilih goal dengan angka")

    if goal == 1:
        user = input("Masukkan nama folder: ")
        print("Sedang membuat folder di workspace...")

        try: 
            os.mkdir(f"workspace/{user}")
            print("Berhasil membuat folder")
        except FileExistsError:
            print("Folder sudah ada")
        except Exception as e:
            print(f"ERROR: {e}")
    elif goal == 2:
        tree("workspace")
        print("Di atas adalah structur folder workspace")
        user = input("Mau buat file dimana dan nama nya apa (lokasi-file nama-file)? ")

        lokasi_file = user.split()[0]
        nama_file = user.split()[1]
        if not lokasi_file and not nama_file:
            print("Format yang anda masukkan salah")
        else:
            print("Sedang membuat file")
            try:
                with open(f"workspace/{lokasi_file}/{nama_file}", "w") as f:
                    f.write("Ini file anda")
                print("File berhasil dibuat")
            except FileExistsError:
                print("File sudah ada")
            except Exception as e:
                print(f"ERROR: {e}")

    # print("Berpikir...")
    # print(llm("halo"))

if __name__=="__main__":
    main()