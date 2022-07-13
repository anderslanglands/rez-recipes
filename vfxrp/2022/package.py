name = "vfxrp"
version = "2022"


@early()
def requires():
    req = [
        "python-3.9",
        "pyqt5-5.15",
        "pyside2-5.15",
        "numpy-1.20",
        "openexr-3.1",
        "ptex-2.4",
        "osd-3.4",
        "openvdb-9",
        "alembic-1.8",
        "ocio-2.1",
        "boost-1.76",
        "tbb-2020.3",
    ]

    import platform
    if platform.system() == "Windows":
        req += ["vs-2019"]
    else:
        req += ["cxx11abi-0"]

    return req

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
            ["platform-linux", "arch-x86_64", "cfg"],
            ["platform-windows", "arch-AMD64", "cfg"],
        ]

