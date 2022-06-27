name = "tbb"
version = "2020.3"

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.TBB_ROOT = "{root}"
    env.TBB_ROOT_DIR = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin/intel64/vc14")


build_command = """
Move-Item -Path {root}/tbb/* -Destination {install_path}
"""


def pre_cook():
    download_and_unpack(f"https://github.com/oneapi-src/oneTBB/releases/download/v{version}/tbb-{version}-win.zip")
