from cx_Freeze import Executable, setup
import sys

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("main.py", base=base, icon="./static/icons/plant.ico", target_name="Lab Data Merger")]

includefiles = [
    "static",
    ".gitignore",
    "fungi_id.py",
    "README.md",
    "requirements.txt",
    "sh_taxonomy_qiime_ver9_99_29.11.2022.txt"
]

packages = [
    "tkinter",
    "os",
    "threading",
    "pandas",
    "re"
]

options = {
    "build_exe": {
        "packages": packages,
        "include_files": includefiles
    }
}

setup(
    name="Lab Data Merger",
    version="1.0",
    options=options,
    executables=executables,
    author="Matan Naydis",
)