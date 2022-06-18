name = "zlib"
version = "1.2.12"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.ZLIB_ROOT = "{root}"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


build_system = "cmake"


def pre_cook():
    import subprocess as sp

    archive = f"v{version}.tar.gz"
    sp.run(["wget", f"https://github.com/madler/zlib/archive/refs/tags/{archive}"])
    sp.run(["tar", "xf", archive, "--strip", "1"])
