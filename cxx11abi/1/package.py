name = "cxx11abi"
version = "1"

variants = [["platform-linux", "arch-x86_64"]]

build_command = False

def commands():
    env.CXXFLAGS = "-D_GLIBCXX_USE_CXX11_ABI=1"
