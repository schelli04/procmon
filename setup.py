import sys
from cx_Freeze import setup, Executable

build_exe_options = {'packages': ["psutil","socket","mysql.connector","time"],
                     'excludes': ["tkinter"]
                    }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "ProcessMonitor",
      version = "0.2",
      description = "Logt ausgewählte Prozesse in MySQL-DB",
      options = {"build.exe": build_exe_options},
      executables = [Executable("main.py", base = base)]
      )
