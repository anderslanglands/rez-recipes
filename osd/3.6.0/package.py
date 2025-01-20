name = "osd"
version = "3.6.0"

requires = ["imath-3", "ptex-2.4", "zlib-1.2"]


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


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


def commands():
    env.OpenSubdiv_ROOT = "{root}"
    env.OPENSUBDIV_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")


@early()
def build_command():

    config_args = [
        "cmake",
        "{root}",
        "-DCMAKE_INSTALL_PREFIX={install_path}",
        f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
        f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
        "-DNO_EXAMPLES=ON",
        "-DNO_TUTORIALS=ON",
        "-DNO_REGRESSION=ON",
        "-DNO_DOC=ON",
        "-DNO_TESTS=ON",
        "-DNO_GLTESTS=ON",
        "-DBUILD_SHARED_LIBS=ON",
        "-DNO_OPENCL=ON",
    ]

    import platform

    if platform.system() == "Windows":
        config_args += [
            "-G",
            f'{env("REZ_CMAKE_GENERATOR")}',
            "-A",
            "x64",
        ]

    return (
        " ".join(config_args)
        + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
    )


def pre_cook():
    fileversion = f"{version}".replace(".", "_")
    download_and_unpack(
        f"https://github.com/PixarAnimationStudios/OpenSubdiv/archive/refs/tags/v{fileversion}.tar.gz"
    )
