name = "imath"
version = "3.0.5"

build_requires = ["cmake"]

variants = [["platform-windows", "arch-AMD64"]]

def commands():
    env.Imath_ROOT = "{root}"
    env.IMATH_HOME = "{root}"
    env.IMATH_DIR = "{root}"
    env.IMATH_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}/lib/cmake")
    env.PATH.append("{root}/bin")


def pre_cook():
    import os, shutil

    print('PRECOOK MOTHERFUCKER')

    def download_file(url, local_dir):
        import urllib.request, shutil, os

        print(f"Downloading {url}...")
        filename = os.path.join(local_dir, os.path.basename(url))
        with urllib.request.urlopen(url) as resp, open(filename, "wb") as f:
            shutil.copyfileobj(resp, f)
        return filename

    fn = download_file(
        f"https://github.com/AcademySoftwareFoundation/Imath/archive/refs/tags/v3.0.5.tar.gz",
        os.getcwd(),
    )
    shutil.unpack_archive(fn)

    archive_dir = "Imath-3.0.5"
    tmp_archive_dir = f"_tmp_rez_cook_{archive_dir}"
    shutil.move(archive_dir, tmp_archive_dir)
    for file in os.listdir(tmp_archive_dir):
        shutil.move(os.path.join(tmp_archive_dir, file), file)
    
    shutil.rmtree(tmp_archive_dir)
    os.remove(fn)

    print("Installing...")
