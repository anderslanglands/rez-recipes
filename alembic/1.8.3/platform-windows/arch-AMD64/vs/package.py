name = "alembic"
version = "1.8.3"

requires = ["imath"]
build_requires = ["cmake", "vs"]


@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.ALEMBIC_ROOT = "{root}"
    env.ALEMBIC_DIR = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")


config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    "-DCMAKE_MODULE_PATH=$env:CMAKE_MODULE_PATH",
    "-DCMAKE_BUILD_TYPE=Release",
    "-DUSE_TESTS=OFF",
    "-DUSE_PYALEMBIC=OFF",
    " -G Ninja",
]

build_command = (
    " ".join(config_args) + " && cmake --build . --target install --config Release"
)


def pre_cook():
    download_and_unpack(
        f"https://github.com/alembic/alembic/archive/refs/tags/{version}.zip"
    )
