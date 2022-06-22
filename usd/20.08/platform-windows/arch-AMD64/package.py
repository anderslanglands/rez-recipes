name = "usd"
version = "20.08"

requires = ["openimageio-2.3", "opensubdiv-3.4", "tbb-2020", "glew-2.1", "Jinja2-3.1", "PySide2-5.15", "PyOpenGL-3.1", 'numpy-1.21']
build_requires = ["vs", "cmake"]

variants = [["platform-windows", "arch-AMD64"]]

def commands():
    env.USD_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")
    env.PATH.prepend("{root}/lib")
    env.PYTHONPATH.prepend("{root}/lib/python")

build_system_args = [
    "-DTBB_ROOT_DIR=$env:TBB_ROOT",
    "-DOPENEXR_LOCATION=$env:OPENEXR_ROOT",
    "-DOPENSUBDIV_ROOT_DIR=$env:OPENSUBDIV_ROOT",
    "-DPTEX_LOCATION=$env:Ptex_ROOT",
    "-DOIIO_LOCATION=$env:OpenImageIO_ROOT",
    "-DBOOST_ROOT=$env:Boost_ROOT",
]


def pre_cook():
    download_and_unpack(
        f"https://github.com/PixarAnimationStudios/USD/archive/refs/tags/v{version}.tar.gz"
    )
