name = "jpegturbo"
version = "2.0.6"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.JPEGTurbo_ROOT = "{root}"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


def pre_cook():
    import subprocess as sp

    archive = f"{version}.tar.gz"
    sp.run(
        ["wget", f"https://github.com/libjpeg-turbo/libjpeg-turbo/archive/refs/tags/{archive}"]
    )
    sp.run(["tar", "xf", archive, "--strip", "1"])
