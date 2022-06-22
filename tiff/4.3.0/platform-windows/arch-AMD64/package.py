name = "tiff"
version = "4.3.0"

requires = ["zlib-1.2", "jpegturbo-2.0"]
build_requires = ["cmake", "vs"]

variants = [["platform-windows", "arch-AMD64"]]

def commands():
    env.LIBTIFF_ROOT = "{root}"
    env.TIFF_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")


def pre_cook():
    archive = f"libtiff-v{version}.tar.gz"
    download_and_unpack(f"https://gitlab.com/libtiff/libtiff/-/archive/v{version}/{archive}")
    