name = "zlib"
version = "1.2.12"

build_requires = ["cmake"]

variants = [
    ["platform-linux", "arch-x86_64", "cxx11abi", "cfg"],
    ["platform-windows", "arch-AMD64", "vs", "cfg"],
]
