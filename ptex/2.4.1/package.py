name = "ptex"
version = "2.4.1"

requires = ["zlib-1.2"]


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
            ["platform-linux", "arch-x86_64", "cxx11abi", "cfg"],
            ["platform-windows", "arch-AMD64", "vs", "cfg"],
        ]


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


def commands():
    env.PATH.prepend("{root}/bin")
    env.PATH.prepend("{root}/lib")
    env.Ptex_ROOT = "{root}"

    import platform

    if platform.system() == "Linux":
        env.LD_LIBRARY_PATH.prepend("{root}/lib")


@early()
def build_command():
    config_args = [
        "cmake",
        "{root}",
        "-DCMAKE_INSTALL_PREFIX={install_path}",
        f'-DCMAKE_MODULE_PATH="{env("CMAKE_MODULE_PATH")}"',
        f'-DCMAKE_BUILD_TYPE="{env("REZ_BUILD_CONFIG")}"',
    ]

    import platform

    if platform.system() == "Windows":
        config_args += [
            "-G",
            f'{env("REZ_CMAKE_GENERATOR")}',
            "-A",
            "x64",
            "-DPTEX_BUILD_STATIC_LIBS=OFF",
        ]

    return (
        " ".join(config_args)
        + f" && cmake --build . --target install --config {env('REZ_BUILD_CONFIG')}"
    )


def pre_cook():
    download_and_unpack(f"https://github.com/wdas/ptex/archive/refs/tags/v{version}.zip")
    patch(
"""
diff --git a/CMakeLists.txt b/CMakeLists.txt
index 4c7e0c3..a933eea 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -33,9 +33,7 @@ enable_testing()
 # Setup platform-specific threading flags.
 find_package(Threads REQUIRED)
 
-# Use pkg-config to create a PkgConfig::Ptex_ZLIB imported target
-find_package(PkgConfig REQUIRED)
-pkg_checK_modules(Ptex_ZLIB REQUIRED zlib IMPORTED_TARGET)
+find_package(ZLIB REQUIRED)
 
 
 if (NOT DEFINED PTEX_SHA)
diff --git a/src/build/ptex-config.cmake b/src/build/ptex-config.cmake
index dfe2851..5e63f07 100644
--- a/src/build/ptex-config.cmake
+++ b/src/build/ptex-config.cmake
@@ -8,9 +8,7 @@ set(THREADS_PREFER_PTHREAD_FLAG ON)
 
 find_dependency(Threads REQUIRED)
 
-# Provide PkgConfig::ZLIB to downstream dependents
-find_dependency(PkgConfig REQUIRED)
-pkg_checK_modules(Ptex_ZLIB REQUIRED zlib IMPORTED_TARGET)
+find_package(ZLIB REQUIRED)
 
 set_and_check(Ptex_DIR @PACKAGE_CMAKE_INSTALL_PREFIX@)
 set_and_check(Ptex_LIBRARY_DIRS @PACKAGE_CMAKE_INSTALL_LIBDIR@)
diff --git a/src/ptex/CMakeLists.txt b/src/ptex/CMakeLists.txt
index e2e1bfd..4dfe372 100644
--- a/src/ptex/CMakeLists.txt
+++ b/src/ptex/CMakeLists.txt
@@ -23,7 +23,7 @@ if(PTEX_BUILD_STATIC_LIBS)
     PRIVATE
         ${CMAKE_CURRENT_SOURCE_DIR})
     target_link_libraries(Ptex_static
-        PUBLIC Threads::Threads PkgConfig::Ptex_ZLIB)
+        PUBLIC Threads::Threads ZLIB::ZLIB)
     install(TARGETS Ptex_static EXPORT Ptex DESTINATION ${CMAKE_INSTALL_LIBDIR})
 endif()
 
@@ -39,7 +39,7 @@ if(PTEX_BUILD_SHARED_LIBS)
             ${CMAKE_CURRENT_SOURCE_DIR})
     target_compile_definitions(Ptex_dynamic PRIVATE PTEX_EXPORTS)
     target_link_libraries(Ptex_dynamic
-        PUBLIC Threads::Threads PkgConfig::Ptex_ZLIB)
+        PUBLIC Threads::Threads ZLIB::ZLIB)
     install(TARGETS Ptex_dynamic EXPORT Ptex DESTINATION ${CMAKE_INSTALL_LIBDIR})
 endif()
 
diff --git a/src/utils/CMakeLists.txt b/src/utils/CMakeLists.txt
index d0295cb..f6bd83d 100644
--- a/src/utils/CMakeLists.txt
+++ b/src/utils/CMakeLists.txt
@@ -4,6 +4,6 @@ if (PTEX_BUILD_STATIC_LIBS)
     add_definitions(-DPTEX_STATIC)
 endif()
 
-target_link_libraries(ptxinfo ${PTEX_LIBRARY} PkgConfig::Ptex_ZLIB)
+target_link_libraries(ptxinfo ${PTEX_LIBRARY} ZLIB::ZLIB)
 
 install(TARGETS ptxinfo DESTINATION ${CMAKE_INSTALL_BINDIR})
"""
    )
