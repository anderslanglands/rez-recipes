name = "opencolorio"
version = "2.1.2"

requires = ["imath-3.1+<4", "python-3.7+<4"]
build_requires = ["vs", "cmake-3.15+<4"]

variants = [["platform-windows", "arch-AMD64"]]


def commands():
    env.PATH.prepend("{root}/bin")
    env.CMAKE_PREFIX_PATH.append("{root}/bin")
    env.PYTHNONPATH.prepend("{root}/lib/site-packages")


cmake_build_system = "ninja"

build_system_args = [
    "-DPython_ROOT=$env:Python_ROOT",
    "-DPython_EXECUTABLE=$env:Python_EXECUTABLE",
]

def pre_cook():
    import os, shutil

    def download_file(url, local_dir):
        import urllib.request, shutil, os

        print(f"Downloading {url}...")
        filename = os.path.join(local_dir, os.path.basename(url))
        with urllib.request.urlopen(url) as resp, open(filename, "wb") as f:
            shutil.copyfileobj(resp, f)
        return filename

    fn = download_file(
        f"https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/refs/tags/v2.1.2.tar.gz",
        os.getcwd(),
    )
    shutil.unpack_archive(fn)

    archive_dir = "OpenColorIO-2.1.2"
    tmp_archive_dir = f"_tmp_rez_cook_{archive_dir}"
    shutil.move(archive_dir, tmp_archive_dir)
    for file in os.listdir(tmp_archive_dir):
        shutil.move(os.path.join(tmp_archive_dir, file), file)

    shutil.rmtree(tmp_archive_dir)
    os.remove(fn)
