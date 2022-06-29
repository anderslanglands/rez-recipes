name = "webp"
version = "1.1.0"

requires = ["zlib-1.2", "png-1.6", "jpegturbo-2.0", "tiff-4.3"]
build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"], ["platform-windows", "arch-AMD64", "vs"]]

