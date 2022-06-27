name = "glew"
version = "2.1.0"

build_requires = ["vs", "cmake"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]

def commands():
    env.GLEW_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")


build_command = """
cd {root}/build
mkdir build && cd build
cmake ../cmake -GNinja -DCMAKE_INSTALL_PREFIX={install_path} -DCMAKE_BUILD_TYPE=Release && ninja install
"""


def pre_cook():
    download_and_unpack(f"https://github.com/nigels-com/glew/releases/download/glew-{version}/glew-{version}.zip")
