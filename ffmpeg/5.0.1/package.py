name = "ffmpeg"
version = "5.0.1"


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
            ["platform-linux", "arch-x86_64"],
            ["platform-windows", "arch-AMD64"],
        ]


def commands():
    import platform

    env.FFMPEG_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")


@early()
def build_command():
    import platform

    if platform.system() == "Windows":
        return f'Move-Item -Path "$env:REZ_BUILD_SOURCE_PATH/ffmpeg-master-latest-win64-lgpl-shared/*" -Destination $env:REZ_BUILD_INSTALL_PATH'
    else:
        return f"mv $REZ_BUILD_SOURCE_PATH/ffmpeg-master-latest-linux64-lgpl-shared/* $REZ_BUILD_INSTALL_PATH"


def pre_cook():
    import platform

    if platform.system() == "Windows":
        fn = "ffmpeg-master-latest-win64-lgpl-shared.zip"
    else:
        fn = "ffmpeg-master-latest-linux64-lgpl-shared.tar.xz"

    download_and_unpack(
        f"https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/{fn}",
        move_up=False,
    )
