name = "openvdb"
version = "9.1.0"

build_requires = ["cmake", "vs"]
requires = ["openexr", "zlib", "boost-1.70+", "tbb", "python", "numpy", "blosc-1.5+"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]

config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    "-DCMAKE_MODULE_PATH=$env:CMAKE_MODULE_PATH",
    "-DCMAKE_BUILD_TYPE=Release",
    " -G Ninja",
    "-DTBB_ROOT=$env:TBB_ROOT",
]

build_command = " ".join(config_args) + " && cmake --build . --target install --config Release --parallel $env:REZ_BUILD_THREAD_COUNT"

def pre_cook():
    download_and_unpack(
        "https://github.com/AcademySoftwareFoundation/openvdb/archive/refs/tags/v9.1.0.zip"
    )
