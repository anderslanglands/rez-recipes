name = "cmake"
version = "3.15.6"

requires = ["vs"]

variants = [["platform-windows", "arch-AMD64"]]

def commands():
    env.PATH.prepend("{root}/bin")

build_command = """
echo $env:REZ_BUILD_REQUIRES
echo $env:REZ_BUILD_VARIANT_REQUIRES
"""

def pre_cook():
    download_and_unpack(f"https://github.com/Kitware/CMake/archive/refs/tags/v{version}.tar.gz")
