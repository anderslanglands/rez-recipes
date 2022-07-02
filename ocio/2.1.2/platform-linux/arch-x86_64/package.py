name = "ocio"
version = "2.1.2"

requires = ["imath-3.1.2+<4", "python-3.7+<4"]
build_requires = ["cmake-3.15+<4", "pybind11-2.6.1+"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.PATH.prepend("{root}/bin")
    env.CMAKE_PREFIX_PATH.prepend("{root}/bin")
    env.PYTHNONPATH.prepend("{root}/lib/site-packages")
    env.PKG_CONFIG_PATH.prepend("{root}/bin")

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")

def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")


def pre_cook():
    import subprocess as sp
    sp.run(["wget", f"https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/refs/tags/v{version}.tar.gz"])
    sp.run(["tar", "xf", f"v{version}.tar.gz", "--strip", "1"])
