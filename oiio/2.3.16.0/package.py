name = "oiio"
version = "2.3.16.0"

requires = [
    "boost-1.70+",
    "openexr-3.0+<3.2",
    "ocio-2.0+",
    "tiff-4.3",
    "openjpeg-2.4",
    "jpegturbo-2.0",
    "png-1.6",
    "raw-0.21",
    "python",
    "pybind11-2.8",
    "webp-1.1",
    "zlib-1.2",
    "ptex-2.4",
    "gif-5.2.1",
    "tbb",
]

hashed_variants = True


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
        req = ["cfg", "boost", "tbb", "openexr", "ocio", "python", "ptex"]
        return [x + req for x in [
                ["platform-linux", "arch-x86_64", "cxx11abi"],
                ["platform-windows", "arch-AMD64", "vs"],
            ]
        ]


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


def commands():
    import os

    def envvar(var: str):
        import platform

        if platform.system() == "Windows":
            return f"$env:{var}"
        else:
            return f"${var}"

    env.OpenImageIO_ROOT = "{root}"
    env.OPENIMAGEIO_HOME = "{root}"
    env.OPENIMAGEIO_DIR = "{root}"
    env.OPENIMAGEIO_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.prepend("{root}/bin")

    env.PYTHONPATH.prepend(f"{{root}}/lib/python{envvar('PYTHON_MAJMIN_VERSION')}/site-packages")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/bin")



config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
    f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    "-DBUILD_DOCS=OFF",
    "-DOIIO_BUILD_TESTS=OFF",
    "-DBUILD_TESTING=OFF",
    f'-DPython_ROOT="{env("Python_ROOT")}"',
    f'-DPython_EXECUTABLE="{env("Python_EXECUTABLE")}"',
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    archive = f"v{version}.tar.gz"
    download_and_unpack(
        f"https://github.com/OpenImageIO/oiio/archive/refs/tags/{archive}"
    )
