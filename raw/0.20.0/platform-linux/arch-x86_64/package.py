name = "raw"
version = "0.20.0"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]

build_command = f"""
aclocal
autoreconf --install
./configure --prefix={{install_path}} && make -j$REZ_BUILD_THREAD_COUNT install
"""

def commands():
    env.LibRaw_ROOT = "{root}"
    env.LibRaw_LIBRARY_DIR = "{root}/lib"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")

def pre_cook():
    import subprocess as sp, os
    os.chdir(build_path)
    archive = f"{version}.tar.gz"
    sp.run(["wget", f"https://github.com/LibRaw/LibRaw/archive/refs/tags/{archive}"])
    sp.run(["tar", "xf", archive, "--strip", "1"])
    