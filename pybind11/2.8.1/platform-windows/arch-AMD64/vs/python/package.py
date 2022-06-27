name = "pybind11"
version = "2.8.1"

build_requires = ["cmake", "python-3"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.pybind11_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")

build_system = "cmake"
build_system_args = ["-DPYBIND11_TEST=OFF", "-DPYTHON_EXECUTABLE=$env:Python_EXECUTABLE"]

def pre_cook():
    import subprocess as sp

    archive = f"v{version}.tar.gz"
    download_and_unpack(f"https://github.com/pybind/pybind11/archive/refs/tags/{archive}")
