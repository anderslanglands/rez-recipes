name = "ffmpeg"
version = "5.0.1"

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.FFMPEG_ROOT = "{root}"
    env.TBB_ROOT_DIR = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")


build_command = """
Move-Item -Path {root}/ffmpeg-n5.0.1-7-g7389a49fd3-win64-lgpl-shared-5.0/* -Destination {install_path}
"""


def pre_cook():
    download_and_unpack(f"https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2022-06-29-12-34/ffmpeg-n5.0.1-7-g7389a49fd3-win64-lgpl-shared-5.0.zip", move_up=False)

