name = "pugixml"
version = "1.14"


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
    env.PUGIXML_ROOT = "{root}"
    env.PUGIXML_ROOT_DIR = "{root}"
    env.PATH.prepend("{root}/bin")
    env.CMAKE_PREFIX_PATH.append("{root}/bin")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")
        env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")


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
    download_and_unpack(
        f"https://github.com/zeux/pugixml/releases/download/v{version}/pugixml-{version}.tar.gz"
    )