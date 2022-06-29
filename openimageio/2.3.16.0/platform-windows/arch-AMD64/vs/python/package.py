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
    "raw-0.21",
    "pybind11-2.8",
    "webp-1.1",
    "zlib-1.2",
    "ptex-2.4",
    "gif-5.2.1",
]

build_requires = ["cmake", "vs"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]

def commands():
    env.OpenImageIO_ROOT = "{root}"
    env.OPENIMAGEIO_HOME = "{root}"
    env.OPENIMAGEIO_DIR = "{root}"
    env.OPENIMAGEIO_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/lib/python3.7/site-packages")


build_system = "cmake"
# cmake_build_system = "ninja"
child_build_args = ["-DBUILD_DOCS=OFF", "-DOIIO_BUILD_TESTS=OFF"]


def pre_cook():
    archive = f"v{version}.tar.gz"
    download_and_unpack(f"https://github.com/OpenImageIO/oiio/archive/refs/tags/{archive}")
