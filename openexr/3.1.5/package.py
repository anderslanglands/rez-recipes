name = "openexr"
version = "3.1.5"

build_requires = ["cmake"]
requires = ["imath-3.1", "zlib-1.2"]

variants = [
    ["platform-linux", "arch-x86_64", "cxx11abi", "cfg"], 
    ["platform-windows", "arch-AMD64", "vs", "cfg"],
]
