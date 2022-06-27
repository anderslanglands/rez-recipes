name = "boost"
version = "1.79.0"

build_requires = ["vs"]
requires = ["python-<3.8"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


build_command = f"""
cd {{root}}
{{root}}/bootstrap.bat && {{root}}/b2 install --prefix={{install_path}} address-model=64 link=shared threading=multi --layout=system variant=release
"""


def commands():
    env.Boost_ROOT = "{root}"
    env.BOOST_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")
    env.CMAKE_PREFIX_PATH.append("{root}/lib/cmake/Boost-1.79.0")


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
        f"https://boostorg.jfrog.io/artifactory/main/release/1.79.0/source/boost_1_79_0.tar.bz2",
        os.getcwd(),
    )
    shutil.unpack_archive(fn)
