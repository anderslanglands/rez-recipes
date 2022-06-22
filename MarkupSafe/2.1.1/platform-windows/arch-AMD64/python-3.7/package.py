name = "MarkupSafe"
version = "2.1.1"

requires = ["python"]
variants = [
    ["platform-windows", "arch-AMD64", "python-3.7"],
]

build_command = """
python -m pip install --prefix {install_path}
"""

def commands():
    env.PYTHONPATH.prepend("{root}/python")
