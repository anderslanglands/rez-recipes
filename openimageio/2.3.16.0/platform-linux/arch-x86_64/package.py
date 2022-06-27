name = "openimageio"
version = "2.3.16.0"

requires = [
    "boost-1.70",
    "openexr-3.0+<3.2",
    "opencolorio-2.0+<2.2",
    "tiff-4.3",
    "openjpeg-2.4",
    "jpegturbo-2.0",
    "png-1.6",
    "raw-0.20",
    "pybind11-2.8",
    "webp-1.1",
    "zlib-1.2",
    "ptex-2.4",
    "gif-5.2.1",
]

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.OpenImageIO_ROOT = "{root}"
    env.OPENIMAGEIO_HOME = "{root}"
    env.OPENIMAGEIO_DIR = "{root}"
    env.OPENIMAGEIO_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.append("{root}/bin")

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


build_system = "cmake"
child_build_args = ["-DBUILD_DOCS=OFF", "-DOIIO_BUILD_TESTS=OFF"]


def pre_cook():
    import subprocess as sp

    archive = f"v{version}.tar.gz"
    sp.run(["wget", f"https://github.com/OpenImageIO/oiio/archive/refs/tags/{archive}"])
    sp.run(["tar", "xf", archive, "--strip", "1"])
