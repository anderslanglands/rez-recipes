name = "gif"
version = "5.2.1"

build_requires = ["cmake", "vs"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]

def commands():
    env.GIF_ROOT = "{root}"
    env.GIF_DIR = "{root}"
    env.PATH.prepend("{root}")

build_system = "cmake"

def pre_cook():
    fetch_repository("https://gitlab.com/anderslanglands/giflib.git")
