name = "openexr"
version = "3.1.5"

requires = ["imath-3.1", "zlib-1.2"]

@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["cmake", "vs"]
    else:
        return ["cmake"]


@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    else:
        # Otherwise tell rez-cook what variants we are capable of building
        return [
            ["platform-linux", "arch-x86_64", "cxx11abi", "cfg"],
            ["platform-windows", "arch-AMD64", "vs", "cfg"],
        ]


def commands():
    import platform 

    env.OPENEXR_ROOT = "{root}"
    env.OPENEXR_HOME = "{root}"
    env.OPENEXR_DIR = "{root}"
    env.OPENEXR_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.prepend("{root}/bin")

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")

def env(var: str):
    import platform
    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"

config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
    f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    download_and_unpack(f"https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v{version}.tar.gz")
