name = "webp"
version = "1.1.0"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.WebP_ROOT = "{root}"
    env.WEBP_ROOT = "{root}"
    env.WEBP_INCLUDE_PATH = "{root}/include"
    env.WEBP_LIBRARY_PATH = "{root}/lib"
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


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
    import subprocess as sp

    archive = f"v{version}.tar.gz"
    sp.run(
        ["wget", f"https://github.com/webmproject/libwebp/archive/refs/tags/{archive}"]
    )
    sp.run(["tar", "xf", archive, "--strip", "1"])
