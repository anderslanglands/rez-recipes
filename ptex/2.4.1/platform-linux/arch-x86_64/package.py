name = "ptex"
version = "2.4.1"

requires = ["zlib-1.2"]
build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]

def commands():
    env.PATH.prepend("{root}/bin")
    env.Ptex_ROOT = "{root}"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")
        env.LDFLAGS.prepend("-L{root}/lib64 -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib64")

build_system = "cmake"


def pre_cook():
    import subprocess as sp
    archive = f"v{version}.tar.gz"
    sp.run(["wget", f"https://github.com/wdas/ptex/archive/refs/tags/{archive}"])
    sp.run(["tar", "xf", archive, "--strip", "1"])
    