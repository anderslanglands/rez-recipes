name = "glew"
version = "2.2.0"

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
    env.GLEW_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")

    import platform
    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")


build_command = """
cd {root}/build
mkdir build && cd build
cmake ../cmake -GNinja -DCMAKE_INSTALL_PREFIX={install_path} -DCMAKE_BUILD_TYPE=Release && ninja install
"""


def pre_cook():
    download_and_unpack(f"https://github.com/nigels-com/glew/releases/download/glew-{version}/glew-{version}.zip")
