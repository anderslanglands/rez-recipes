name = "vfxrp"
version = "2021"


@early()
def requires():
    req = [
        "python-3.7",
        "pyqt5-5.15",
        "pyside2-5.15",
        "numpy-1.19",
        "openexr-3",     # These aren't legit, but the whole 2->3 bifurcation is a PITA
        "imath-3",
        "ptex-2.3+",     # should be 2.3 but building it on windows is a PITA
        "osd-3.4",
        "openvdb-8",
        "alembic-1.8",   # Neither is this legit
        "ocio-2.0",
        "boost-1.73",
        "tbb-2020.2+",
    ]

    import platform
    if platform.system() == "Windows":
        req += ["vs-2017", "platform-windows", "arch-AMD64"]
    else:
        req += ["cxx11abi-0", "platform-linux", "arch-x86_64"]

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
            ["platform-linux", "arch-x86_64", "cxx11abi-0", "python-3.7", "cfg"],
            ["platform-windows", "arch-AMD64", "vs-2017", "python-3.7", "cfg"],
        ]

