name = "gif"
version = "5.2.1"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.GIF_ROOT = "{root}"
    env.GIF_DIR = "{root}"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")

build_command = f"""
make -j$REZ_BUILD_THREAD_COUNT && 
make install PREFIX=$REZ_BUILD_INSTALL_PATH -j$REZ_BUILD_THREAD_COUNT
"""


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


def pre_cook():
    import subprocess as sp, os
    os.chdir(build_path)

    archive = f"giflib-{version}.tar.gz"
    sp.run(
        ["wget", f"https://gitlab.com/koreader/giflib/-/archive/{version}/{archive}"]
    )
    sp.run(["tar", "xf", archive, "--strip", "1"])
