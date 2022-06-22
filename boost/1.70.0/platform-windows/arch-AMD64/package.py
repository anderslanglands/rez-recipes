name = "boost"
version = "1.70.0"

build_requires = ["vs"]
requires = ["python-<3.8"]

variants = [["platform-windows", "arch-AMD64"]]

build_command = f"""
cd {{root}}/boost_1_70_0
{{root}}/boost_1_70_0/bootstrap.bat && {{root}}/boost_1_70_0/b2 install --prefix={{install_path}} address-model=64 link=shared threading=multi --layout=tagged
"""

def commands():
    env.Boost_ROOT = "{root}"
    env.BOOST_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.prepend('{root}/lib/cmake/Boost-1.70.0')
    env.PATH.prepend("{root}/lib")

def pre_build_commands():
    download_and_unpack(
        f"https://boostorg.jfrog.io/artifactory/main/release/1.70.0/source/boost_1_70_0.tar.bz2",
    )

