name = "ptex"
version = "2.4.1"

requires = ["zlib-1.2"]
build_requires = ["cmake", "vs"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.PATH.prepend("{root}/bin")
    env.PATH.prepend("{root}/lib")
    env.Ptex_ROOT = "{root}"


build_system = "cmake"
build_system_args = ["-DPTEX_BUILD_STATIC_LIBS=OFF"]


def pre_cook():
    fetch_repository("https://github.com/anderslanglands/ptex.git")
