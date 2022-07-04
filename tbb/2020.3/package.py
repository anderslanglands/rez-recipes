name = "tbb"
version = "2020.3"

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
    env.TBB_ROOT = "{root}"
    env.TBB_ROOT_DIR = "{root}"
    env.TBB_LIBRARY_DIR = "{root}/lib/intel64/vc14"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.PATH.prepend("{root}/bin/intel64/vc14")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/bin/intel64/vc14")

def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"

@early()
def build_command():
    import platform 

    if platform.system() == "Windows":
        return """
        Move-Item -Path \"$env:REZ_BUILD_SOURCE_PATH/tbb/*\" -Destination \"$env:REZ_BUILD_INSTALL_PATH\"
        # Copy binaries up to make VDB happy
        Copy-Item -Path \"$env:REZ_BUILD_INSTALL_PATH/lib/intel64/vc14/*\" -Destination \"$env:REZ_BUILD_INSTALL_PATH/lib\"
        Copy-Item -Path \"$env:REZ_BUILD_INSTALL_PATH/bin/intel64/vc14/*\" -Destination \"$env:REZ_BUILD_INSTALL_PATH/bin\"
        """
    else:
        return '''
        cp -r $REZ_BUILD_SOURCE_PATH/tbb/* $REZ_BUILD_INSTALL_PATH
        cp -r $REZ_BUILD_INSTALL_PATH/lib/intel64/gcc4.8/* $REZ_BUILD_INSTALL_PATH/lib/
        '''


def pre_cook():
    import platform 

    if platform.system() == "Windows":
        download_and_unpack(f"https://github.com/oneapi-src/oneTBB/releases/download/v{version}/tbb-{version}-win.zip", move_up=False)
    else:
        download_and_unpack(f"https://github.com/oneapi-src/oneTBB/releases/download/v{version}/tbb-{version}-lin.tgz", move_up=False)
