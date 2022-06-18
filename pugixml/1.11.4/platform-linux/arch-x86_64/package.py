name = "pugixml"
version = "1.11.4"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.pugixml_ROOT = "{root}"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")

build_system = "cmake"
child_build_args = ["-DBUILD_SHARED_LIBS=ON", "-DBUILD_TESTS=OFF"]

def pre_cook():
    import subprocess as sp

    archive = f"v{version}.tar.gz"
    sp.run(["wget", f"https://github.com/zeux/pugixml/archive/refs/tags/{archive}"])
    sp.run(["tar", "xf", archive, "--strip", "1"])
