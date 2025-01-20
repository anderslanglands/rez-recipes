name = "cgstubs"
version = "1.0.0"

requires = ["python-3.7+"]


@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    else:
        # Otherwise tell rez-cook what variants we are capable of building
        return [
            ["python"],
        ]


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


STUBS = [
    "usd",
    "houdini",
    "katana",
    "mari",
    "nuke",
    "opencolorio",
    "PySide2",
    "substance_painter",
]


def get_build_command():
    build_commands = []
    for stub in STUBS:
        build_commands.append(
            f"rez-env python-{env('PYTHON_VERSION')} -- "
            f"python -m pip install types-{stub} "
            f"--target='{{install_path}}/{stub}' --no-deps --use-pep517")
    return " && ".join(build_commands)


build_command = get_build_command()


def pre_cook():
    import os
    for stub in STUBS:
        os.makedirs(os.path.join(install_path, stub), exist_ok=True)


def post_cook():
    import os
    import shutil

    for stub in STUBS:
        parent = os.path.join(install_path, stub)
        for filename in os.listdir(parent):
            filepath = os.path.join(parent, filename)
            if filename.endswith("dist-info"):
                shutil.rmtree(filepath)
            if filename.endswith("-stubs"):
                shutil.move(filepath, filepath[:-6])


def commands():
    import os

    STUBS = [
        "usd",
        "houdini",
        "katana",
        "mari",
        "nuke",
        "opencolorio",
        "PySide2",
        "substance_painter",
    ]
    for stub in STUBS:
        env.PYTHONPATH.prepend(os.path.join("{root}", stub))
