name = "ocio"
version = "2.0.4"

requires = ["openexr-2.4|3", "python-3.7+"]


@early()
def build_requires():
    import platform

    if platform.system() == "Windows":
        return ["cmake", "vs", "pybind11-2.6.1+"]
    else:
        return ["cmake", "pybind11-2.6.1+"]


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
            ["platform-linux", "arch-x86_64", "cxx11abi", "python", "cfg"],
            ["platform-windows", "arch-AMD64", "vs", "python", "cfg"],
        ]


def commands():
    env.OCIO_ROOT = "{root}"
    env.OpenColorIO_ROOT = "{root}"
    env.PATH.prepend("{root}/bin")
    env.CMAKE_PREFIX_PATH.append("{root}/bin")
    env.PYTHNONPATH.prepend("{root}/lib/site-packages")

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")


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
    f'-DPython_ROOT={env("Python_ROOT")}',
    f'-DPython_EXECUTABLE={env("Python_EXECUTABLE")}',
    "-DOCIO_BUILD_TESTS=OFF",
    "-DOCIO_BUILD_GPU_TESTS=OFF",
    " -G Ninja",
]

build_command = (
    " ".join(config_args)
    + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
)


def pre_cook():
    download_and_unpack(f"https://github.com/AcademySoftwareFoundation/OpenColorIO/archive/refs/tags/v{version}.zip")

    # patch to fix build type and missing cxxflags in built deps
    patch(
"""
diff --git a/CMakeLists.txt b/CMakeLists.txt
index c54dbbf6..984b1f87 100755
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -79,16 +79,6 @@ endif()
 
 set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
 
-# Is that a valid build type?
-
-if(NOT "${CMAKE_BUILD_TYPE}" IN_LIST CMAKE_CONFIGURATION_TYPES)
-    string(REPLACE ";" ", " _CMAKE_CONFIGURATION_TYPES_STR "${CMAKE_CONFIGURATION_TYPES}")
-    message(FATAL_ERROR 
-            "CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} is unsupported. Supported values are: ${_CMAKE_CONFIGURATION_TYPES_STR}.")
-endif()
-
-# Is that in debug mode?
-
 set(_BUILD_TYPE_DEBUG OFF)
 if(CMAKE_BUILD_TYPE MATCHES "[Dd][Ee][Bb][Uu][Gg]")
     set(_BUILD_TYPE_DEBUG ON)
diff --git a/share/cmake/modules/Findpystring.cmake b/share/cmake/modules/Findpystring.cmake
index 5975da43..97784fc9 100644
--- a/share/cmake/modules/Findpystring.cmake
+++ b/share/cmake/modules/Findpystring.cmake
@@ -87,6 +87,7 @@ if(NOT pystring_FOUND)
         endif()
 
         string(STRIP "${pystring_CXX_FLAGS}" pystring_CXX_FLAGS)
+        set(pystring_CXX_FLAGS " ${pystring_CXX_FLAGS} $ENV{CXXFLAGS}")
 
         set(pystring_CMAKE_ARGS
             ${pystring_CMAKE_ARGS}
diff --git a/share/cmake/modules/Findyaml-cpp.cmake b/share/cmake/modules/Findyaml-cpp.cmake
index e0de62e2..1bdc5f4a 100644
--- a/share/cmake/modules/Findyaml-cpp.cmake
+++ b/share/cmake/modules/Findyaml-cpp.cmake
@@ -172,6 +172,7 @@ if(NOT yaml-cpp_FOUND)
         endif()
 
         string(STRIP "${yaml-cpp_CXX_FLAGS}" yaml-cpp_CXX_FLAGS)
+        set(yaml-cpp_CXX_FLAGS " ${yaml-cpp_CXX_FLAGS} $ENV{CXXFLAGS}")
 
         set(yaml-cpp_CMAKE_ARGS
             ${yaml-cpp_CMAKE_ARGS}

"""
    )