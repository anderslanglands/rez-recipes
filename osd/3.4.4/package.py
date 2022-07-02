name = "osd"
version = "3.4.4"

requires = ["imath-3.1", "ptex-2.4", "zlib-1.2"]
build_requires = ["vs", "cmake"]

variants = [["platform-windows", "arch-AMD64", "vs"], ["platform-linux", "arch-x86_64"]]