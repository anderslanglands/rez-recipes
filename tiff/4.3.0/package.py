name = "tiff"
version = "4.3.0"

requires = ["zlib-1.2", "jpegturbo-2.0"]
build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"], ["platform-windows", "arch-AMD64", "vs"]]

