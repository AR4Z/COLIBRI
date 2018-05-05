import sys
from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))


os.environ["TCL_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ["TK_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

build_exe_options = {'packages':['vlc','tkinter.messagebox', 'fitz', 'mutagen', 'tkinter.filedialog', 'tkinter.ttk', 'sqlite3', 'pdf2image', 'pytesseract', 'numpy'],
                     'include_files':[os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                    os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                                      "frames", "utils","text.txt", "count.txt", "..\\img", "bin", "lame.zip", "poppler-0.51.zip"]}
base = None

if sys.platform == "Win32":
    base = "Win32GUI"


setup( name="swsw",
       version="0.1",
       description="swswswsor",
       options = {"build_exe": build_exe_options},
       executables = [Executable("main.py", base=base)])
