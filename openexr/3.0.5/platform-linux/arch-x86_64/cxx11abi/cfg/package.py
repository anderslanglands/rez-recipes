name = "openexr"
version = "3.0.5"

build_requires = ["cmake", "imath-3.0"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.OpenEXR_ROOT = "{root}"
    env.OPENEXR_HOME = "{root}"
    env.OPENEXR_DIR = "{root}"
    env.OPENEXR_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
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
    download_and_unpack(f"https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v{version}.tar.gz")

