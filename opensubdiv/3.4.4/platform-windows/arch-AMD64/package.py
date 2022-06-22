name = "opensubdiv"
version = "3.4.4"

requires = ["imath-3.1", "ptex-2.4", "zlib-1.2"]
build_requires = ["vs", "cmake"]

variants = [["platform-windows", "arch-AMD64"]]


def commands():
    env.OpenSubdiv_ROOT = "{root}"
    env.OPENSUBDIV_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")


build_system = "cmake"
build_system_args = [
    "-DNO_EXAMPLES=ON",
    "-DNO_TUTORIALS=ON",
    "-DNO_REGRESSION=ON",
    "-DNO_DOC=ON",
    "-DNO_TESTS=ON",
    "-DNO_GLTESTS=ON",
    "-DBUILD_SHARED_LIBS=ON",
]


def pre_cook():
    download_and_unpack(
        "https://github.com/anderslanglands/OpenSubdiv/archive/refs/tags/recipe-3_4_4.tar.gz"
    )
