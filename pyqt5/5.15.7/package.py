name = "pyqt5"
version = "5.15.7"

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
            ["platform-linux", "arch-x86_64", "cxx11abi", "python"],
            ["platform-windows", "arch-AMD64", "vs", "python"],
        ]


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


build_command = f"""
rez-env python-{env('PYTHON_VERSION')} -- python -m pip install {name}=={version} --target="{{install_path}}" --no-deps --use-pep517
"""


def commands():
    env.PYTHONPATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")
