name = "imath"
version = "3.1.5"

build_requires = ["cmake"]


@early()
def variants():
    import os, ast

    cook_variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [cook_variant]


def commands():
    env.Imath_ROOT = "{root}"
    env.IMATH_HOME = "{root}"
    env.IMATH_DIR = "{root}"
    env.IMATH_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}/lib/cmake")
    env.PATH.append("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/bin")


config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    '-DCMAKE_MODULE_PATH="$CMAKE_MODULE_PATH"',
    '-DCMAKE_BUILD_TYPE="$REZ_BUILD_CONFIG"',
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + " && cmake --build . --target install --config $env:REZ_BUILD_CONFIG"
)


def pre_cook():
    download_and_unpack(
        f"https://github.com/AcademySoftwareFoundation/Imath/archive/refs/tags/v{version}.tar.gz"
    )
