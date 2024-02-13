name = "ocio"
version = "2.3.1"

requires = ["openexr-2.4|3.1.2+", "python-3.7+"]

hashed_variants = True


@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["cmake", "vs", "pybind11-2.6.1+"]
    else:
        return ["cmake", "pybind11-2.6.1+"]


@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    else:
        # Otherwise tell rez-cook what variants we are capable of building
        req = ["cfg", "openexr", "python"]
        return [x + req for x in [
                ["platform-linux", "arch-x86_64", "cxx11abi"],
                ["platform-windows", "arch-AMD64", "vs"],
            ]
        ]


def commands():
    env.OCIO_ROOT = "{root}"
    env.OpenColorIO_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")
    env.CMAKE_PREFIX_PATH.append("{root}/bin")
    env.PYTHONPATH.prepend("{root}/lib/site-packages")
    env.OCIO_LOAD_DLLS_FROM_PATH = "1"

    import platform

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
    f'-DPython_ROOT={env("Python_ROOT")}',
    f'-DPython_EXECUTABLE={env("Python_EXECUTABLE")}',
    "-DOCIO_BUILD_TESTS=OFF",
    "-DOCIO_BUILD_GPU_TESTS=OFF",
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    download_and_unpack(
        f"https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/refs/tags/v{version}.tar.gz"
    )
