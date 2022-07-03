name = "blosc"
version = "1.21.1"


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

    env.BLOSC_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")

    if platform.system():
        env.LD_LIBRARY_PATH.prepend("{root}/lib")


config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    "-DCMAKE_MODULE_PATH=$env:CMAKE_MODULE_PATH",
    "-DCMAKE_BUILD_TYPE=Release",
    " -G Ninja",
]

build_command = (
    " ".join(config_args) + " && cmake --build . --target install --config Release"
)


def pre_cook():
    download_and_unpack(
        f"https://github.com/Blosc/c-blosc/archive/refs/tags/v{version}.zip"
    )
