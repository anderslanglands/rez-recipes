name = "openexr"
version = "3.1.5"

build_requires = ["cmake", "imath-3.1+<3.2"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.OpenEXR_ROOT = "{root}"
    env.OPENEXR_HOME = "{root}"
    env.OPENEXR_DIR = "{root}"
    env.OPENEXR_LOCATION = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}/lib/cmake")
    env.PATH.append("{root}/bin")

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


def pre_cook():
     import subprocess as sp
     sp.run(["wget", f"https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v{version}.tar.gz"])
     sp.run(["tar", "xf", f"v{version}.tar.gz", "--strip", "1"])
    


