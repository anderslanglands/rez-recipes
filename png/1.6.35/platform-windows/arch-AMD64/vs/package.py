name = "png"
version = "1.6.35"

requires = ["zlib-1.2"]
build_requires = ["cmake", "vs"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.PATH.prepend("{root}/bin")
    env.PNG_ROOT = "{root}"
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")


def pre_cook():
    archive = f"v{version}.tar.gz"
    download_and_unpack(
        f"https://github.com/glennrp/libpng/archive/refs/tags/{archive}"
    )