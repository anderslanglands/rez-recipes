name = "cmake"
version = "3.23.2"

variants = [["platform-linux", "arch-x86_64"]]

def commands():
    env.PATH.prepend("{root}/bin")

build_command = """
mv {root}/cmake-{version}-linux-x86_64/* {install_path}
"""

def pre_cook():
    download_and_unpack(f"https://github.com/Kitware/CMake/releases/download/v{version}/cmake-{version}-linux-x86_64.tar.gz", move_up=False)


