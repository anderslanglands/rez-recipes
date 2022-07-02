name = "cmake"
version = "3.23.2"

requires = ["vs"]

variants = [["platform-windows", "arch-AMD64"]]

def commands():
    env.PATH.prepend("{root}/bin")

build_command = """
Move-Item -Path {root}/cmake-{version}-windows-x86_64/* -Destination {install_path}
"""

def pre_cook():
    download_and_unpack(f"https://github.com/Kitware/CMake/releases/download/v{version}/cmake-{version}-windows-x86_64.zip", move_up=False)

