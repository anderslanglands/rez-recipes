name = "openimageio"
version = "2.3.16"

requires = [
    "boost-1.70",
    "openexr-3.0+<3.2",
    "opencolorio-2.0+<2.2",
    "tiff-4.3",
    "openjpeg-2.4",
    "jpegturbo-2.0",
    "png-1.6",
    "raw-0.20+<0.22",
    "pybind11-2.8",
    "webp-1.1",
    "zlib-1.2",
    "ptex-2.4",
    "gif-5.2.1",
]

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"], ["platform-windows", "arch-AMD64", "vs", "python"]]
