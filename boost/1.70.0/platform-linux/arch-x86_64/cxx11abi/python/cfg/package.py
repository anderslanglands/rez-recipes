name = "boost"
version = "1.70.0"

build_requires = ["cmake"]
requires = ["python-<3.8"]

@early()
def variants():
    import os, ast

    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


build_command = f"""
cd {{root}} && \
./bootstrap.sh --prefix={{install_path}} && \
./b2 install --prefix={{install_path}} address-model=64 link=shared threading=multi --layout=system variant=$REZ_BUILD_CONFIG
"""

def commands():
    env.Boost_ROOT = "{root}"
    env.BOOST_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend("{root}")
    env.LD_LIBRARY_PATH.prepend("{root}/lib")


def pre_cook():
    download_and_unpack(
        f"https://boostorg.jfrog.io/artifactory/main/release/{version}/source/boost_{version.replace('.', '_')}.tar.bz2",
    )