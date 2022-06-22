name = "openjpeg"
version = "2.4.0"

build_requires = ["cmake", "vs"]

variants = [["platform-windows", "arch-AMD64"]]

def commands():
    env.OpenJPEG_ROOT = "{root}"
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")
    env.PATH.prepend("{root}/bin")


def pre_cook():
    archive = f"v{version}.tar.gz"
    download_and_unpack(f"https://github.com/uclouvain/openjpeg/archive/refs/tags/{archive}")
    