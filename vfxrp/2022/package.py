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
        req += ["cxx11abi-1"]

    return req
