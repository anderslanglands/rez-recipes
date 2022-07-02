name = "boost"
version = "1.70.0"

requires = ["python<3.8"]

variants = [
    ["platform-linux", "arch-x86_64", "cxx11abi", "python", "cfg"],
    ["platform-windows", "arch-AMD64", "vs", "python", "cfg"],
]
