name = "neovim"
version = "0.7.2"

@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    else:
        # Otherwise tell rez-cook what variants we are capable of building
        req = ["python"]
        return [x + req for x in [
                ["platform-linux", "arch-x86_64", "cxx11abi"],
                ["platform-windows", "arch-AMD64", "vs"],
            ]
        ]

@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["python-3", "vs"]
    else:
        return ["python-3"]


@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["cmake", "vs"]
    else:
        return ["cmake"]


def commands():
    env.PATH.prepend("{root}/bin")

build_system = "cmake"

def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"

@early()
def build_command():

    config_args = [
        "cmake",
        "{root}",
        "-DCMAKE_INSTALL_PREFIX={install_path}",
        f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
        f'-DCMAKE_BUILD_TYPE=Release',
        "-DUSE_BUNDLED_LUA=ON",
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
        f" echo {env('REZ_BUILD_CONFIG')} && cd {env('REZ_BUILD_SOURCE_PATH')}/build && " 
        + " ".join(config_args)
        + f" && cmake --build . --target install --config Release"
    )

def pre_cook():
    fetch_repository("https://github.com/neovim/neovim", branch = f"v{version}")
