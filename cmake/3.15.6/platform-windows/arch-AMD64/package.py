name = "cmake"
version = "3.15.6"

requires = ["vs"]

variants = [["platform-windows", "arch-AMD64"]]

def commands():
    env.PATH.prepend("{root}/bin")

build_command = """
Move-Item -Path {root}/cmake-3.15.6-win64-x64/* -Destination {install_path}
"""

def pre_cook():
    download_and_unpack(f"https://cmake.org/files/v3.15/cmake-3.15.6-win64-x64.zip", move_up=False)
