name = "usd"
version = "20.08"

requires = ["openimageio", "opensubdiv", "tbb"]
build_requires = ["vs", "cmake"]

variants = [["platform-windows", "arch-AMD64"], ["platform-linux", "arch-x86_64"]]

