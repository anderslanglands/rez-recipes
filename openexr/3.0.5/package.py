name = "openexr"
version = "3.0.5"

build_requires = ["cmake"]
requires = ["imath-3.0"]

variants = [["platform-linux", "arch-x86_64"], ["platform-windows", "arch-AMD64", "vs"]]
