name = "zlib"
version = "1.2.12"

build_requires = ["cmake", "vs"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.PATH.prepend("{root}/bin")
    env.ZLIB_ROOT = "{root}"
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")


config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    '-DCMAKE_MODULE_PATH="$env:CMAKE_MODULE_PATH"',
    '-DCMAKE_BUILD_TYPE="$env:REZ_BUILD_CONFIG"',
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + " && cmake --build . --target install --config $env:REZ_BUILD_CONFIG"
)

def pre_cook():
    download_and_unpack(f"https://github.com/madler/zlib/archive/refs/tags/v{version}.tar.gz")
