name = "imath"
version = "3.1.5"

build_requires = ["cmake", "cfg"]

variants = [
    ["platform-linux", "arch-x86_64", "cxx11abi", "cfg"],
    ["platform-windows", "arch-AMD64", "vs", "cfg"],
]
