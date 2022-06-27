name = "webp"
version = "1.1.0"

build_requires = ["cmake", "vs", "zlib-1.2", "png-1.6", "jpegturbo-2.0", "tiff-4.3"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.WebP_ROOT = "{root}"
    env.WEBP_ROOT = "{root}"
    env.WEBP_INCLUDE_PATH = "{root}/include"
    env.WEBP_LIBRARY_PATH = "{root}/lib"
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")
    env.PATH.prepend("{root}/bin")


build_system_args = [
    "-DJPEG_INCLUDE_DIR=${env:JPEGTurbo_ROOT}/include",
    "-DJPEG_LIBRARY=${env:JPEGTurbo_ROOT}/lib/jpeg.lib",
    "-DTIFF_INCLUDE_DIR=${env:TIFF_ROOT}/include",
    "-DTIFF_LIBRARY=${env:TIFF_ROOT}/lib/tiff.lib",
]

build_system = "cmake"
child_build_args = [
    "-DBUILD_SHARED_LIBS=ON",
    "-DBUILD_TESTS=OFF",
    "-DWEBP_BUILD_ANIM_UTILS=OFF",
    "-DWEBP_BUILD_CWEBP=OFF",
    "-DWEBP_BUILD_VWEBP=OFF",
    "-DWEBP_BUILD_GIF2WEBPx=OFF",
    "-DDWEBP_BUILD_IMG2WEBP=OFF",
    "-DWEBP_BUILD_EXTRAS=OFF",
    "-DDBUILD_SHARED_LIBS=ON",
]


def pre_cook():
    archive = f"v{version}.tar.gz"
    download_and_unpack(
        f"https://github.com/webmproject/libwebp/archive/refs/tags/{archive}"
    )
