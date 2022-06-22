name = "jpegturbo"
version = "2.0.6"

build_requires = ["cmake", "vs"]

variants = [["platform-windows", "arch-AMD64"]]


def commands():
    env.PATH.prepend("{root}/bin")
    env.JPEGTurbo_ROOT = "{root}"
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")


def pre_cook():
    import os

    archive = f"{version}.tar.gz"
    download_and_unpack(
        f"https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/{archive}"
    )

