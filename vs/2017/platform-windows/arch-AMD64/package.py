from rez.utils.lint_helper import env, building, scope  # make linter happy

name = "vs"
version = "2017"
description = """
Microsoft Visual Studio (Reference package)

This is a somewhat hacky package that triggers the
Visual Studio Developer command prompt (VsDevCmd.bat)
and retrieves any environment variables that it sets
so we can apply them with this package environment.

"""

variants = [['platform-windows', 'arch-AMD64']]

build_command = False

tools = ["cl", "msbuild", "cmake"]


def commands():
    import os

    global env
    global alias

    import subprocess

    env.REZ_CMAKE_GENERATOR = "Visual Studio 15 2017"

    def collect_environment(cmd):
        # Return the new resulting environment variables from the command
        result = subprocess.check_output("%s & set" % cmd).decode('utf-8')

        devenv = {}
        for line in result.splitlines():
            if not line.strip():
                continue
            if line.startswith("*") or line.startswith("_"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            # In some cases values end with \\ for no reason. Let's force remove it only
            # from those that do not seem to refer to a path (don't have :\ in it, like C:\)
            if not ":\\" in value and value.endswith("\\"):
                value = value[:-1]

            paths = [x.strip() for x in value.split(";") if x.strip()]

            # Keep only the paths that are not in the current os.environ to ensure we only
            # get the newly set data from the .bat running through subprocess
            old = set(os.getenv(key, "").split(";"))
            if old:
                paths = [p for p in paths if p not in old]
                if not paths:
                    continue

            devenv[key] = ";".join(paths)

        return devenv

    def find_cmd(version):
        import os

        base_path = f"C:/Program Files (x86)/Microsoft Visual Studio/{version}"
        for edition in ["Enterprise", "Professional", "Community"]:
            path = os.path.join(base_path, edition, "VC", "Auxiliary", "Build", "vcvars64.bat")
            if os.path.isfile(path):
                return path

    dev_cmd = find_cmd(this.version)
    if dev_cmd is None:
        raise rez.exceptions.InvalidPackageError(
            f"Could not find Visual Studio {this.version}"
        )

    devenv = collect_environment(dev_cmd)

    for key, paths in sorted(devenv.items()):

        if len(paths.split(os.pathsep)) == 1 and key not in os.environ:
            # Simply set single values as opposed to appending
            # to ensure it's not suddenly prefixed with ;
            if key.upper() == "PATH":
                env.PATH = paths
            else:
                env[key] = paths
        else:
            if key.upper() == "PATH":
                env.PATH.append(paths)
            else:
                env[key].append(paths)


def pre_cook():
    import os
    def find_cmd(version):
        import os

        base_path = f"C:/Program Files (x86)/Microsoft Visual Studio/{version}"
        for edition in ["Enterprise", "Professional", "Community"]:
            path = os.path.join(base_path, edition, "VC", "Auxiliary", "Build", "vcvars64.bat")
            if os.path.isfile(path):
                return path

    path = find_cmd(version)
    if not os.path.isfile(path):
        raise RuntimeError("Could not find Visual Studio 2017")

