name = "zlib"
version = "1.2.12"

build_requires = ["cmake", "vs"]

variants = [["platform-windows", "arch-AMD64"]]


def commands():
    env.PATH.prepend("{root}/bin")
    env.ZLIB_ROOT = "{root}"
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")

build_system = "cmake"


def pre_cook():
    archive = f"v{version}.tar.gz"
    download_and_unpack(f"https://github.com/madler/zlib/archive/refs/tags/{archive}")
