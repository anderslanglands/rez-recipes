import platform

name = "python"
version = "3.10.5"

variants = [["platform-linux", "arch-x86_64"], ["platform-windows", "arch-AMD64"]]


# def commands():
#     env.PATH.append("{root}")
#     env.PYTHONHOME = "{root}"
#     env.PYTHONPATH = "{root}"


# if platform.system().lower() == "windows":
#     build_command = """
#     ..\\python-3.10.5-amd64.exe /passive InstallAllUsers=0 TargetDir={install_path}
#     """


# def pre_build_commands():
#     import os, shutil, sys

#     print(sys.version)

#     def download_file(url, local_dir):
#         import urllib.request, shutil, os

#         print(f"Downloading {url}...")
#         filename = os.path.join(local_dir, os.path.basename(url))
#         with urllib.request.urlopen(url) as resp, open(filename, "wb") as f:
#             shutil.copyfileobj(resp, f)
#         return filename

#     fn = download_file(
#         "https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe", os.getcwd()
#     )
#     print("Installing...")
