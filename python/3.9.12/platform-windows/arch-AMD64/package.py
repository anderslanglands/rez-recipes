name = "python"
version = "3.9.12"

variants = [["platform-windows", "arch-AMD64"]]


def commands():
    env.PATH.append("{root}")
    env.PYTHONHOME = "{root}"
    env.PYTHONPATH = "{root}"

    env.Python_ROOT = "{root}"
    env.Python_EXECUTABLE = "{root}/python.exe"

build_command = f"""
{{root}}\\python-{version}-amd64.exe /passive InstallAllUsers=0 TargetDir={{install_path}} Include_doc=0 Include_launcher=0 Include_test=0
"""


def pre_build_commands():
    import os

    def download_file(url, local_dir):
        import urllib.request, shutil, os

        print(f"Downloading {url}...")
        filename = os.path.join(local_dir, os.path.basename(url))
        with urllib.request.urlopen(url) as resp, open(filename, "wb") as f:
            shutil.copyfileobj(resp, f)
        return filename

    _ = download_file(
        f"https://www.python.org/ftp/python/{this.version}/python-{this.version}-amd64.exe",
        os.getcwd(),
    )
    print("Installing...")
