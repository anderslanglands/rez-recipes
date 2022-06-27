name = "python"
version = "3.9.12"

variants = [["platform-windows", "arch-AMD64"]]


def commands():
    env.PATH.append("{root}")
    env.PYTHONHOME = "{root}"
    env.PYTHONPATH = "{root}"

    env.Python_ROOT = "{root}"
    env.Python_EXECUTABLE = "{root}/python.exe"


build_command = f"""
Move-Item -Path {{root}}/python-{{version}}/* -Destination {{install_path}}
"""


def pre_cook():
    download_and_unpack(
        f"https://github.com/anderslanglands/rez-recipes/releases/download/python-3.7.9-3.9.12/python-{version}.zip",
        move_up=False,
    )
