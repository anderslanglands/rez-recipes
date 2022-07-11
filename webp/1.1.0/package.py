name = "webp"
version = "1.1.0"

requires = ["zlib-1.2", "png-1.6", "jpegturbo-2.0", "tiff-4.3", "gif-5.2"]

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
    env.WebP_ROOT = "{root}"
    env.WEBP_ROOT = "{root}"
    env.WEBP_INCLUDE_PATH = "{root}/include"
    env.WEBP_LIBRARY_PATH = "{root}/lib"
    env.PATH.prepend("{root}/bin")

    import platform
    if platform.system() == "Linux":
        env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")
        env.LD_LIBRARY_PATH.prepend("{root}/lib")


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
    "-DBUILD_SHARED_LIBS=ON",
    "-DBUILD_TESTS=OFF",
    "-DWEBP_BUILD_ANIM_UTILS=OFF",
    "-DWEBP_BUILD_CWEBP=OFF",
    "-DWEBP_BUILD_VWEBP=OFF",
    "-DWEBP_BUILD_GIF2WEBPx=OFF",
    "-DDWEBP_BUILD_IMG2WEBP=OFF",
    "-DWEBP_BUILD_EXTRAS=OFF",
    f'-DJPEG_INCLUDE_DIR={env("JPEGTurbo_ROOT")}/include',
    f'-DJPEG_LIBRARY={env("JPEGTurbo_ROOT")}/lib/jpeg.lib',
    f'-DTIFF_INCLUDE_DIR={env("TIFF_ROOT")}/include',
    f'-DTIFF_LIBRARY={env("TIFF_ROOT")}/lib/tiff.lib',
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)

@early()
def build_command():
    import platform

    config_args = [
        "cmake",
        "{root}",
        "-DCMAKE_INSTALL_PREFIX={install_path}",
        f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
        f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
        "-DBUILD_SHARED_LIBS=OFF",
        "-DBUILD_TESTS=OFF",
        "-DWEBP_BUILD_ANIM_UTILS=OFF",
        "-DWEBP_BUILD_CWEBP=OFF",
        "-DWEBP_BUILD_VWEBP=OFF",
        "-DWEBP_BUILD_GIF2WEBPx=OFF",
        "-DDWEBP_BUILD_IMG2WEBP=OFF",
        "-DWEBP_BUILD_EXTRAS=OFF",
        "-G Ninja",
    ]

    return (
        " ".join(config_args)
        + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
    )


def pre_cook():
    download_and_unpack(
        f"https://github.com/webmproject/libwebp/archive/refs/tags/v{version}.tar.gz"
    )
