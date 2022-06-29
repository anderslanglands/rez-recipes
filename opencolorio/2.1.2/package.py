name = "opencolorio"
version = "2.1.2"

requires = ["imath-3.1.2+<4", "python-3.7+<4"]
build_requires = ["pybind11-2.6.1+"]

variants = [["platform-linux", "arch-x86_64"], ["platform-windows", "arch-AMD64", "vs", "python"]]