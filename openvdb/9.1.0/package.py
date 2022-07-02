name = "openvdb"
version = "9.1.0"

build_requires = ["cmake"]
requires = ["openexr", "zlib", "boost-1.70+", "tbb", "python", "numpy", "blosc-1.5+"]

variants = [["platform-windows", "arch-AMD64", "vs", "python"]]