name = "usd"
version = "20.08"

requires = ["openimageio-2.3", "opensubdiv-3.4", "tbb-2020", "glew-2.1"]
build_requires = ["vs", "cmake"]

variants = [
    ["platform-windows", "arch-AMD64", "vs", "python"], 
    ["platform-linux", "arch-x86_64"],
    ["platform-linux", "arch-x86_64", "python-3.7"],
]

