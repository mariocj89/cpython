from pathlib import Path
import os
import shutil
import site
import subprocess
import sys

sitecustomize_dir_path = Path(site.getsitepackages()[0]) / "__sitecustomize__"
usercustomize_dir_path = Path(site.getusersitepackages()) / "__sitecustomize__"
sitecustomize_py_path = Path(site.getsitepackages()[0]) / "sitecustomize.py"
usercustomize_py_path = Path(site.getusersitepackages()) / "usercustomize.py"
pth_dir_path = Path(site.getsitepackages()[0])
pth_prefix = "test-pth-"
pth_content = "import time; x = time.time() ** 5#; print(__file__)"
sc_content = pth_content

def cleanup_interpreter():
    shutil.rmtree(usercustomize_dir_path, ignore_errors=True)
    shutil.rmtree(sitecustomize_dir_path, ignore_errors=True)
    for file_ in [
            *list(pth_dir_path.glob(f"{pth_prefix}*.pth")),
            sitecustomize_py_path,
            usercustomize_py_path,
    ]:
        try:
            os.remove(file_)
        except FileNotFoundError:
            pass

def run_benchmark():
    output = subprocess.check_output([
            sys.executable, "./measure-startup-time.py"
        ],
        stderr=subprocess.STDOUT,
    )
    return int(output)

def make_sitecustomize_folder():
    sitecustomize_dir_path.mkdir()

def make_usercustomize_folder():
    usercustomize_dir_path.mkdir()


_COUNTER = 0


def make_pth_file():
    global _COUNTER
    _COUNTER += 1
    pth_path = pth_dir_path / f"{pth_prefix}{_COUNTER}.pth"
    pth_path.write_text(pth_content)


def make_sitecustomize_file():
    global _COUNTER
    _COUNTER += 1
    path = sitecustomize_dir_path / f"file-{_COUNTER}.py"
    path.write_text(sc_content)


def make_usersitecustomize_file():
    global _COUNTER
    _COUNTER += 1
    path = usercustomize_dir_path / f"file-{_COUNTER}.py"
    path.write_text(sc_content)


def make_sitecustomize_py():
    sitecustomize_py_path.write_text(sc_content)


def make_usercustomize_py():
    usercustomize_py_path.write_text(sc_content)


def main():
    cleanup_interpreter()

    print("Test 1")
    print(run_benchmark())
    cleanup_interpreter()

    print("Test 2")
    make_sitecustomize_folder()
    print(run_benchmark())
    cleanup_interpreter()

    print("Test 3")
    make_sitecustomize_folder()
    make_pth_file()
    print(run_benchmark())
    cleanup_interpreter()

    print("Test 4")
    make_sitecustomize_folder()
    make_sitecustomize_file()
    print(run_benchmark())
    cleanup_interpreter()

    print("Test 5")
    make_sitecustomize_folder()
    make_sitecustomize_py()
    make_usercustomize_py()
    print(run_benchmark())
    cleanup_interpreter()

    print("Test 6")
    make_sitecustomize_folder()
    make_usercustomize_folder()
    make_sitecustomize_file()
    make_usersitecustomize_file()
    print(run_benchmark())
    cleanup_interpreter()

    print("Test 7")
    make_sitecustomize_folder()
    for _ in range(50):
        make_pth_file()
    print(run_benchmark())
    cleanup_interpreter()

    print("Test 8")
    make_sitecustomize_folder()
    for _ in range(50):
        make_sitecustomize_file()
    print(run_benchmark())
    cleanup_interpreter()

if __name__ == '__main__':
    main()
