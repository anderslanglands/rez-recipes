name = "python"
version = "3.7.9"


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
        return [
            ["platform-linux", "arch-x86_64"],
            ["platform-windows", "arch-AMD64"],
        ]


def commands():
    import platform

    env.PYTHONHOME = "{root}"
    env.Python_ROOT = "{root}"

    env.PYTHON_VERSION = "{version}"
    env.PYTHON_MAJMIN_VERSION = ".".join(f"{version}".split(".")[:2])
    
    if platform.system() == "Windows":
        env.PATH.append("{root}")
        env.PYTHONPATH = "{root}"
        env.Python_EXECUTABLE = "{root}/python.exe"
    else:
        env.PATH.append("{root}/bin")
        env.LD_LIBRARY_PATH.prepend("{root}/lib")
        env.Python_EXECUTABLE = "{root}/bin/python"
        env.PYTHONPATH = "{root}/lib/python3.7"


def pre_cook():
    import platform

    if platform.system() == "Windows":
        download_and_unpack(
            f"https://github.com/anderslanglands/rez-recipes/releases/download/python-3.7.9-3.9.12/python-{version}.zip",
            move_up=False,
        )
    else:
        download_and_unpack(
            f"https://www.python.org/ftp/python/{version}/Python-{version}.tgz"
        )


@early()
def build_command():
    import platform

    if platform.system() == "Windows":
        return f'Move-Item -Path "$env:REZ_BUILD_SOURCE_PATH/python-{version}/*" -Destination "$env:REZ_BUILD_INSTALL_PATH"'
    else:
        return f"""
            cd $REZ_BUILD_SOURCE_PATH && \
            ./configure  --prefix=$REZ_BUILD_INSTALL_PATH \
                --enable-optimizations \
                --enable-ipv6 \
                --enable-shared \
                --with-dbmliborder=gdbm:ndbm:bdb \
                --with-system-expat \
                --with-system-ffi \
                --with-ensurepip \
                --without-pymalloc \
                --with-computed-gotos=yes && \
            make install -j$REZ_BUILD_THREAD_COUNT && \
            ln -s $REZ_BUILD_INSTALL_PATH/bin/python3 $REZ_BUILD_INSTALL_PATH/bin/python && \
            """
