name = "usd"
version = "20.08"

requires = [
    "openimageio-2.3",
    "opensubdiv-3.4",
    "tbb-2020",
    "glew-2.1",
    "jinja2-3.1",
    "pyside2-5.15",
    "pyopengl-3.1",
    "numpy-1.21",
]
build_requires = ["vs", "cmake"]

variants = [
    ["platform-windows", "arch-AMD64", "vs", "python"], 
    ["platform-linux", "arch-x86_64"],
    ["platform-linux", "arch-x86_64", "python-3.7"],
]

