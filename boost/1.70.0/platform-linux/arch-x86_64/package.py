name = "boost"
version = "1.70.0"

build_requires = ["cmake"]
requires = ["python-<3.8"]

variants = [["platform-linux", "arch-x86_64"]]

build_command = f"""
./bootstrap.sh --prefix={{install_path}} && \
./b2 install --prefix={{install_path}} address-model=64 link=shared threading=multi --layout=system
"""

def commands():
    env.Boost_ROOT = "{root}"
    env.BOOST_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.append('{root}/lib/cmake/Boost-{version}')

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")

def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


def pre_cook():
     import subprocess as sp, os
     uversion = version.replace(".", "_")
     archive = f"boost_{uversion}.tar.bz2"
     os.chdir(build_path)
     sp.run(["wget", f"https://boostorg.jfrog.io/artifactory/main/release/{version}/source/{archive}"])
     sp.run(["tar", "xf", f"{archive}", "--strip", "1"])

    #  env.REZ_BOOST_BUILD_CMD_WGET = f"wget https://boostorg.jfrog.io/artifactory/main/release/{version}/source/{archive}"
    #  env.REZ_BOOST_BUILD_CMD_TAR = f"tar xf {archive} --strip 1"
    

# def pre_build_commands():
#     import os, shutil

#     def download_file(url, local_dir):
#         import urllib.request, shutil, os

#         print(f"Downloading {url}...")
#         filename = os.path.join(local_dir, os.path.basename(url))
#         with urllib.request.urlopen(url) as resp, open(filename, "wb") as f:
#             shutil.copyfileobj(resp, f)
#         return filename

#     fn = download_file(
#         f"https://boostorg.jfrog.io/artifactory/main/release/1.70.0/source/boost_1_70_0.tar.bz2",
#         os.getcwd(),
#     )
#     shutil.unpack_archive(fn)


