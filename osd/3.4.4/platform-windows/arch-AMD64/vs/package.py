name = "osd"
version = "3.4.4"

requires = ["imath-3.1", "ptex-2.4", "zlib-1.2"]
build_requires = ["vs", "cmake"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.OpenSubdiv_ROOT = "{root}"
    env.OPENSUBDIV_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")


config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    "-DCMAKE_MODULE_PATH=$env:CMAKE_MODULE_PATH",
    "-DCMAKE_BUILD_TYPE=Release",
    "-DREZ_BUILD_INSTALL=$env:REZ_BUILD_INSTALL",
    "-G", "$env:REZ_CMAKE_GENERATOR",
    "-A", "x64",
    "-DNO_EXAMPLES=ON",
    "-DNO_TUTORIALS=ON",
    "-DNO_REGRESSION=ON",
    "-DNO_DOC=ON",
    "-DNO_TESTS=ON",
    "-DNO_GLTESTS=ON",
    "-DBUILD_SHARED_LIBS=ON",
    "-DNO_OPENCL=ON",
]

build_command = " ".join(config_args) + "\n" + "cmake --build . --target INSTALL --config Release"

def pre_cook():
    download_and_unpack(
        "https://github.com/anderslanglands/OpenSubdiv/archive/refs/tags/recipe-3_4_4.tar.gz"
    )
