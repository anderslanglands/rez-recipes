name = "python"
version = "3.9.12"


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

    if platform.system() == "Windows":
        env.PATH.append("{root}")
        env.PYTHONPATH = "{root}"
        env.Python_EXECUTABLE = "{root}/python.exe"
    else:
        env.PATH.append("{root}/bin")
        env.LD_LIBRARY_PATH.prepend("{root}/lib")
        env.Python_EXECUTABLE = "{root}/bin/python3"
        env.PYTHONPATH = "{root}/lib/python3.9"


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


def pre_build_command():
    import platform

    if platform.system() == "Linux":
        env.CFLAGS = " ".join(
            [
                "-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2",
                "-fexceptions -fstack-protector-strong",
                "--param=ssp-buffer-size=4 -grecord-gcc-switches",
                "-m64 -mtune=generic -D_GNU_SOURCE",
                "-fPIC -fwrapv $CFLAGS",
            ]
        )
        env.LDFLAGS = "-Wl,-rpath,$REZ_BUILD_INSTALL_PATH/lib $LDFLAGS"


@early()
def build_command():
    import platform

    if platform.system() == "Windows":
        return f'Move-Item -Path "$env:REZ_BUILD_SOURCE_PATH/python-{version}/*" -Destination "$env:REZ_BUILD_INSTALL_PATH"'
    else:
        return f"""
cd $REZ_BUILD_SOURCE_PATH && \
./configure  --prefix=$REZ_BUILD_INSTALL_PATH \
    --enable-optimizations --enable-ipv6 --enable-shared \
    --with-dbmliborder=gdbm:ndbm:bdb --with-system-expat \
    --with-system-ffi --with-ensurepip --with-computed-gotos=yes && \
make install -j$REZ_BUILD_THREAD_COUNT && \
ln -s $REZ_BUILD_INSTALL_PATH/bin/python3 $REZ_BUILD_INSTALL_PATH/bin/python
"""
