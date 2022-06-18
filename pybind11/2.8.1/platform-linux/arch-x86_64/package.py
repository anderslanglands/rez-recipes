name = "pybind11"
version = "2.8.1"

build_requires = ["cmake", "python-3"]

variants = [["platform-linux", "arch-x86_64"]]


def commands():
    env.pybind11_ROOT = "{root}"

    if building:
        env.LDFLAGS.prepend("-L{root}/lib -Wl,-rpath,{root}/lib")


def pre_build_commands():
    env.LDFLAGS.prepend("-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib")

build_system = "cmake"
child_build_args = ["-DPYBIND11_TEST=OFF", "-DPYTHON_EXECUTABLE=$Python_EXECUTABLE"]

def pre_cook():
    import subprocess as sp

    archive = f"v{version}.tar.gz"
    sp.run(["wget", f"https://github.com/pybind/pybind11/archive/refs/tags/{archive}"])
    sp.run(["tar", "xf", archive, "--strip", "1"])
