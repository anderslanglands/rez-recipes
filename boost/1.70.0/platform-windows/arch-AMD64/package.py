name = "boost"
version = "1.70.0"

build_requires = ["vs"]
requires = ["python-<3.8"]

variants = [["platform-windows", "arch-AMD64"]]

build_command = f"""
cd {{root}}/boost_1_70_0
{{root}}/boost_1_70_0/bootstrap.bat && {{root}}/boost_1_70_0/b2 install --prefix={{install_path}} address-model=64 link=shared threading=multi && move {{install_path}}\\include\\boost-1_70\\boost {{install_path}}\\include\\boost && del /q {{install_path}}\\include\\boost-1_70
"""

def commands():
    env.Boost_ROOT = "{root}"
    env.BOOST_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.append('{root}/lib/cmake/Boost-1.70.0')

def pre_build_commands():
    import os, shutil

    def download_file(url, local_dir):
        import urllib.request, shutil, os

        print(f"Downloading {url}...")
        filename = os.path.join(local_dir, os.path.basename(url))
        with urllib.request.urlopen(url) as resp, open(filename, "wb") as f:
            shutil.copyfileobj(resp, f)
        return filename

    fn = download_file(
        f"https://boostorg.jfrog.io/artifactory/main/release/1.70.0/source/boost_1_70_0.tar.bz2",
        os.getcwd(),
    )
    shutil.unpack_archive(fn)
    print("Installing...")

