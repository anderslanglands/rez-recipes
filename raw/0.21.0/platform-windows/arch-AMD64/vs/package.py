name = "raw"
version = "0.21.0"

requires = ["jpegturbo", "zlib-1.2"]
build_requires = ["cmake", "vs"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.LibRaw_ROOT = "{root}"
    env.LibRaw_LIBRARY_DIR = "{root}/lib"
    env.PATH.prepend("{root}/bin")


build_system_args = [
    "-DJPEG_INCLUDE_DIR=${env:JPEGTurbo_ROOT}/include",
    "-DJPEG_LIBRARY=${env:JPEGTurbo_ROOT}/lib/libjpeg",
]


def pre_cook():
    import subprocess as sp, os, shutil

    sp.run(
        [
            "git",
            "clone",
            "--recursive",
            "--depth",
            "1",
            "-b",
            f"v0.21.0a1",
            "https://github.com/anderslanglands/raw.git",
            "_clone",
        ]
    )

    for f in os.listdir("_clone"):
        shutil.move(os.path.join("_clone", f), f)
