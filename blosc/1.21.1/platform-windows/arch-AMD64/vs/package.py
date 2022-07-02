name = "blosc"
version = "1.21.1"

build_requires = ["cmake", "vs"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.BLOSC_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")

def pre_cook():
    download_and_unpack("https://github.com/Blosc/c-blosc/archive/refs/tags/v1.21.1.zip")