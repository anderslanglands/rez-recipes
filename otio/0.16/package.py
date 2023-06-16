name = "otio"
version = "0.16"

requires = [
    "python",
]

hashed_variants = True


@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["cmake-3.18+", "vs"]
    else:
        return ["cmake-3.18+"]


@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    else:
        # Otherwise tell rez-cook what variants we are capable of building
        req = ["cfg", "python"]
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

    env.OTIO_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.CMAKE_PREFIX_PATH.append("{root}/share")

    env.PYTHONPATH.prepend(f"{{root}}/python")

    import platform

    if platform.system() == "Linux":
        # Shared libraries get put in the python installation for reasons (python-3.8 idiocy?)
        env.LD_LIBRARY_PATH.prepend("{root}/python/opentimelineio")
        env.LD_LIBRARY_PATH.prepend("{root}/python/opentime")



config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
    f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    "-DOTIO_PYTHON_INSTALL=ON",
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    fetch_repository("https://github.com/anderslanglands/OpenTimelineIO.git")

