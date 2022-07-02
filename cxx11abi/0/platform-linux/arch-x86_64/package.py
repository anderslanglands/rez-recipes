name = "cxx11abi"
version = "0"

variants = [["platform-linux", "arch-x86_64"]]

def commands():
    env.CXXFLAGS = "-D_GLIBCXX_USE_CXX11_ABI=0"

build_command = False
