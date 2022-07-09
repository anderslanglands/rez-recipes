name = "vfxrp"
version = "2023"


@early()
def requires():
    req = [
        "python-3.10",
        "pyqt5-5.15",
        "pyside2-5.15",
        "numpy-1.22",
        "openexr-3.2",
        "ptex-2.4",
        "osd-3.4",
        "openvdb-10",
        "alembic-1.8",
        "ocio-2.2",
        "boost-1.79",
        "tbb-2020.3",
    ]

    import platform
    if platform.system() == "Windows":
        req += ["vs-2022"]
    else:
        req += ["cxx11abi-1"]

    return req
