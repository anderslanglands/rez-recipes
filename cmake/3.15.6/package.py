name = "cmake"
version = "3.15.6"


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
            ["platform-linux", "arch-x86_64"],
            ["platform-windows", "arch-AMD64"],
        ]


def commands():
    env.PATH.prepend("{root}/bin")


def pre_cook():
    import platform

    if platform.system() == "Windows":
        archive = f"cmake-{version}-windows-x86_64.zip"
    else:
        archive = f"cmake-{version}-linux-x86_64.tar.gz"

    download_and_unpack(
        f"https://github.com/Kitware/CMake/releases/download/v{version}/{archive}",
        move_up=False,
    )


@early()
def build_command():
    import platform

    if platform.system() == "Windows":
        return f"Move-Item -Path $env:REZ_BUILD_SOURCE_PATH/cmake-{version}-windows-x86_64/* -Destination $env:REZ_BUILD_INSTALL_PATH"
    else:
        return f"mv $REZ_BUILD_SOURCE_PATH/cmake-{version}-linux-x86_64/* $REZ_BUILD_INSTALL_PATH"
