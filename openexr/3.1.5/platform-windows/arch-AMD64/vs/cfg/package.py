name = "openexr"
version = "3.1.5"

build_requires = ["cmake"]
requires = ["imath-3.1", "zlib-1.2"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.OPENEXR_ROOT = "{root}"
    env.OPENEXR_HOME = "{root}"
    env.OPENEXR_DIR = "{root}"
    env.OPENEXR_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}/lib/cmake")
    env.PATH.prepend("{root}/bin")


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
        f"https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v3.1.5.tar.gz",
        os.getcwd(),
    )
    shutil.unpack_archive(fn)

    archive_dir = "openexr-3.1.5"
    tmp_archive_dir = f"_tmp_rez_cook_{archive_dir}"
    shutil.move(archive_dir, tmp_archive_dir)
    for file in os.listdir(tmp_archive_dir):
        shutil.move(os.path.join(tmp_archive_dir, file), file)
    
    shutil.rmtree(tmp_archive_dir)
    os.remove(fn)

    print("Installing...")

