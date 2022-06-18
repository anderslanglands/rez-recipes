name = "imath"
version = "3.1.5"

build_requires = ["cmake"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.Imath_ROOT = "{root}"
    env.IMATH_HOME = "{root}"
    env.IMATH_DIR = "{root}"
    env.IMATH_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}/lib/cmake")
    env.PATH.append("{root}/bin")

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


def pre_cook():
     import subprocess as sp
     sp.run(["wget", f"https://github.com/AcademySoftwareFoundation/Imath/archive/refs/tags/v{version}.tar.gz"])
     sp.run(["tar", "xf", f"v{version}.tar.gz", "--strip", "1"])
    

