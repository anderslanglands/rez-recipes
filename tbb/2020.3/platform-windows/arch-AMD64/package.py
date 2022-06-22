name = "tbb"
version = "2020.3"

variants = [["platform-windows", "arch-AMD64"]]


def commands():
    env.TBB_ROOT = "{root}"
    env.TBB_ROOT_DIR = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin/intel64/vc14")


build_command = """
Move-Item -Path {root}/tbb/* -Destination {install_path}
"""


def pre_cook():
    download_and_unpack(f"https://github.com/oneapi-src/oneTBB/releases/download/v2020.3/tbb-{version}-win.zip")
