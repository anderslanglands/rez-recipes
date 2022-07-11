name = "boost"
version = "1.76.0"

requires = ["python"]


@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["vs"]
    else:
        return []


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
            ["platform-linux", "arch-x86_64", "cxx11abi", "python", "cfg"],
            ["platform-windows", "arch-AMD64", "vs", "python", "cfg"],
        ]


def commands():
    import platform

    env.Boost_ROOT = "{root}"
    env.BOOST_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")

    if platform.system() == "Windows":
        env.PATH.prepend("{root}/lib")
    elif platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")


def pre_cook():
    download_and_unpack(
        f"https://boostorg.jfrog.io/artifactory/main/release/{version}/source/boost_{version.replace('.', '_')}.tar.bz2",
    )


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


@early()
def build_command():
    import platform

    if platform.system() == "Windows":
        return f"cd $env:REZ_BUILD_SOURCE_PATH && ./bootstrap.bat && ./b2 install --prefix=\"$env:REZ_BUILD_INSTALL_PATH\" address-model=64 link=shared --layout=system threading=multi variant=\"$env:REZ_BUILD_CONFIG\" -d0"
    else:
        return f"cd $REZ_BUILD_SOURCE_PATH && ./bootstrap.sh --with-python=$Python_EXECUTABLE && ./b2 install --prefix=$REZ_BUILD_INSTALL_PATH address-model=64 link=shared threading=multi --layout=system variant=$REZ_BUILD_CONFIG -j$REZ_BUILD_THREAD_COUNT -d0 cxxflags=$CXXFLAGS"
