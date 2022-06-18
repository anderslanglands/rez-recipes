name = "ffmpeg"
version = "5.0.1"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.FFMPEG_ROOT = "{root}"
    env.FFmpeg_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


build_command = f"""
./configure --prefix=$REZ_BUILD_INSTALL_PATH && make install -j$REZ_BUILD_THREAD_COUNT
"""


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


def pre_cook():
    import subprocess as sp, os

    os.chdir(build_path)

    archive = f"ffmpeg-{version}.tar.gz"
    sp.run(["wget", f"https://ffmpeg.org/releases/{archive}"])
    sp.run(["tar", "xf", archive, "--strip", "1"])
