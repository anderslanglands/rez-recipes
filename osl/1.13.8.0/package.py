name = "osl"
version = "1.13.8.0"

requires = [
    "oiio",
    "llvm",
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
        req = ["oiio", "llvm"]
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
    def envvar(var: str):
        import platform

        if platform.system() == "Windows":
            return f"$env:{var}"
        else:
            return f"${var}"

    env.OpenShadingLanguage_ROOT = "{root}"
    env.OSL_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.prepend("{root}/bin")

    env.PYTHONPATH.prepend(f"{{root}}/lib/python{envvar('PYTHON_MAJMIN_VERSION')}/site-packages")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")



config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
    f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    "-DCMAKE_CXX_STANDARD=17",
    # "-DCMAKE_CXX_FLAGS=-I/usr/include/c++/11/",
    # "-DLLVM_COMPILE_FLAGS=-I/usr/include/c++/11;-I/usr/include/x86_64-linux-gnu/c++/11",
    "-DUSE_LLVM_BITCODE=OFF",
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    download_and_unpack(
        f"https://github.com/AcademySoftwareFoundation/OpenShadingLanguage/archive/refs/tags/v{version}.tar.gz"
    )

