name = "ocio"
version = "2.2.0"

requires = ["openexr-2.4|3.1.2+", "python-3.7+"]


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
    env.PYTHONPATH.prepend("{root}/lib/site-packages")
    env.OCIO_LOAD_DLLS_FROM_PATH = "1"

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
    fetch_repository("https://github.com/anderslanglands/OpenColorIO.git")

    # patch to fix build type and missing cxxflags in built deps
    patch(
"""diff --git a/CMakeLists.txt b/CMakeLists.txt
index a8b4a3cd..25d7a13b 100755
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -83,24 +83,7 @@ if(NOT DEFINED CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
     set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
 endif()

-# List all the valid build types.
-
-if(NOT DEFINED CMAKE_CONFIGURATION_TYPES)
-    set(CMAKE_CONFIGURATION_TYPES "Debug;Release;MinSizeRel;RelWithDebInfo" CACHE STRING "" FORCE)
-    mark_as_advanced(CMAKE_CONFIGURATION_TYPES)
-endif()
-
-set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
-
-# Is that a valid build type?
-
-if(NOT "${CMAKE_BUILD_TYPE}" IN_LIST CMAKE_CONFIGURATION_TYPES)
-    string(REPLACE ";" ", " _CMAKE_CONFIGURATION_TYPES_STR "${CMAKE_CONFIGURATION_TYPES}")
-    message(FATAL_ERROR 
-            "CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} is unsupported. Supported values are: ${_CMAKE_CONFIGURATION_TYPES_STR}.")
-endif()
-
-# Is that in debug mode?
+# Are we in debug mode?

 set(_BUILD_TYPE_DEBUG OFF)
 if(CMAKE_BUILD_TYPE MATCHES "[Dd][Ee][Bb][Uu][Gg]")
diff --git a/share/cmake/modules/Findpystring.cmake b/share/cmake/modules/Findpystring.cmake
index 702ac1e8..71692bd4 100644
--- a/share/cmake/modules/Findpystring.cmake
+++ b/share/cmake/modules/Findpystring.cmake
@@ -86,6 +86,7 @@ if(NOT pystring_FOUND AND NOT OCIO_INSTALL_EXT_PACKAGES STREQUAL NONE)
         endif()

         string(STRIP "${pystring_CXX_FLAGS}" pystring_CXX_FLAGS)
+        set(pystring_CXX_FLAGS " ${pystring_CXX_FLAGS} $ENV{CXXFLAGS}")

         set(pystring_CMAKE_ARGS
             ${pystring_CMAKE_ARGS}
diff --git a/share/cmake/modules/Findyaml-cpp.cmake b/share/cmake/modules/Findyaml-cpp.cmake
index 023e14fc..4081cf29 100644
--- a/share/cmake/modules/Findyaml-cpp.cmake
+++ b/share/cmake/modules/Findyaml-cpp.cmake
@@ -165,6 +165,7 @@ if(NOT yaml-cpp_FOUND AND NOT OCIO_INSTALL_EXT_PACKAGES STREQUAL NONE)
         endif()

         string(STRIP "${yaml-cpp_CXX_FLAGS}" yaml-cpp_CXX_FLAGS)
+        set(yaml-cpp_CXX_FLAGS " ${yaml-cpp_CXX_FLAGS} $ENV{CXXFLAGS}")

         set(yaml-cpp_CMAKE_ARGS
             ${yaml-cpp_CMAKE_ARGS}
"""
    )