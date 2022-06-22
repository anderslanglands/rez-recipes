name = "tiff"
version = "4.3.0"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]

def commands():
    env.LIBTIFF_ROOT = "{root}"
    env.TIFF_ROOT = "{root}"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")



def pre_cook():
    archive = f"libtiff-v{version}.tar.gz"
    download_and_unpack(f"https://gitlab.com/libtiff/libtiff/-/archive/v{version}/{archive}")
    