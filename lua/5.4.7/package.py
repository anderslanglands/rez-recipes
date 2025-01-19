name = "lua"
version = "5.4.7"

requires = []


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
    env.LUA_ROOT = "{root}"
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


build_command = (
    "cd .. && make install INSTALL_TOP={install_path}"
)


def pre_cook():
    download_and_unpack(
        f"https://www.lua.org/ftp/lua-5.4.7.tar.gz"
    )

