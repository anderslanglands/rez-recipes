name = "openvdb"
version = "11.0.0"

requires = ["openexr", "zlib", "boost-1.70+", "tbb", "python", "numpy", "blosc-1.5+"]

hashed_variants = True

def commands():
    env.OpenVDB_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/lib/python3.7/site-packages")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/bin")


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
        req = ["cfg", "boost", "tbb", "openexr", "python"]
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

config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
    f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    " -G Ninja",
    f'-DTBB_ROOT="{env("TBB_ROOT")}"',
]

build_command = " ".join(config_args) + f" && cmake --build . --target install --config Release --parallel {env('REZ_BUILD_THREAD_COUNT')}"

def pre_cook():
    download_and_unpack(
        f"https://github.com/AcademySoftwareFoundation/openvdb/archive/refs/tags/v{version}.zip"
    )
