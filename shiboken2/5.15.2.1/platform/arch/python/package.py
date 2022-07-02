name = "shiboken2"
version = "5.15.2.1"

requires = ["python-3.7+"]

@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    print(f"VARIANT: {variant}")

    return [variant]

build_command = f"""
rez-env python-$env:REZ_BUILD_PYTHON_VERSION -- python -m pip install {name}=={version} --target="{{install_path}}" --no-deps --use-pep517
"""

def commands():
    env.PYTHONPATH.prepend("{root}")

