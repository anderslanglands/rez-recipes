name = "usd"
version = "23.11"

requires = [
    "openexr-3",
    "boost-1.70+",
    "ocio-2",
    "oiio-2",
    "osd-3.4+",
    "tbb-2020",
    "glew-2.1",
    "jinja2-3.1",
    "pyside6",
    "pyopengl-3.1",
    "numpy",
    "python-3",
]


hashed_variants = True

@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["cmake", "vs"]
    else:
        return ["cmake"]


@early()
def variants():
    import os, ast

    cook_variant = os.getenv("REZ_COOK_VARIANT")
    if cook_variant:
        # If we're building the package, we want to use the variant supplied to us
        return [ast.literal_eval(cook_variant)]
    else:
        # Otherwise tell rez-cook what variants we are capable of building
        req = ["cfg", "boost", "tbb", "openexr", "ocio", "oiio", "python", "ptex", "osd"]
        return [x + req for x in [
                ["platform-linux", "arch-x86_64", "cxx11abi"],
                ["platform-windows", "arch-AMD64", "vs"],
            ]
        ]


def commands():
    env.USD_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")
    env.PATH.prepend("{root}/lib")
    env.PYTHONPATH.prepend("{root}/lib/python")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")
        env.PYOPENGL_PLATFORM = "glx"


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


config_args = [
    "cmake",
    "{root}",
    "-DCMAKE_INSTALL_PREFIX={install_path}",
    f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
    f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    f'-DTBB_ROOT_DIR="{env("TBB_ROOT")}"',
    f'-DOPENEXR_LOCATION="{env("OPENEXR_ROOT")}"',
    f'-DOPENSUBDIV_ROOT_DIR="{env("OPENSUBDIV_ROOT")}"',
    f'-DPTEX_LOCATION="{env("Ptex_ROOT")}"',
    f'-DOIIO_LOCATION="{env("OpenImageIO_ROOT")}"',
    f'-DBOOST_ROOT="{env("Boost_ROOT")}"',
    f'-DPython_ROOT="{env("Python_ROOT")}"',
    f'-DPython3_ROOT="{env("Python_ROOT")}"',
    f'-DPython_EXECUTABLE="{env("Python_EXECUTABLE")}"',
    f'-DPython3_EXECUTABLE="{env("Python_EXECUTABLE")}"',
    "-DPXR_BUILD_DOCUMENTATION=FALSE",
    "-DPXR_BUILD_TESTS=FALSE",
    "-DPXR_BUILD_EXAMPLES=FALSE",
    "-DPXR_USE_PYTHON_3=ON",
    "-DCMAKE_CXX_STANDARD=17",
    # Fix for boost inserting the wrong library names into the libs with 
    # --layout=system...
    f'-DCMAKE_CXX_FLAGS="-DBOOST_ALL_NO_LIB -D__TBB_show_deprecation_message_task_H -DBOOST_BIND_GLOBAL_PLACEHOLDERS -Wno-class-memaccess {env("CXXFLAGS")}"',
    " -G Ninja",
]

import platform

if platform.system() == "Linux":
    config_args.append(f'-DCMAKE_CXX_FLAGS="-DBOOST_ALL_NO_LIB -D__TBB_show_deprecation_message_task_H -DBOOST_BIND_GLOBAL_PLACEHOLDERS -Wno-class-memaccess {env("CXXFLAGS")}"')
else:
    config_args.append(f'-DCMAKE_CXX_FLAGS="-DBOOST_ALL_NO_LIB -D__TBB_show_deprecation_message_task_H -DBOOST_BIND_GLOBAL_PLACEHOLDERS {env("CXXFLAGS")}"')


build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    download_and_unpack(
        f"https://github.com/PixarAnimationStudios/USD/archive/refs/tags/v{version}.tar.gz"
    )
