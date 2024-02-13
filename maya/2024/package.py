name = "maya"
version = "2024"


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
            ["platform-linux"],
            ["platform-windows"],
        ]


def env(var: str):
    import platform

    if platform.system() == "Windows":
        return f"$env:{var}"
    else:
        return f"${var}"


def pre_cook():
    import os

    unpack(
        os.path.expanduser(f"~/Downloads/Autodesk_Maya_{version}-Linux_64bit.tgz"),
        extract_dir=build_path,
    )


build_command = (
    "{build_path}/houdini.install "
    "--accept-EULA 2021-10-13 "
    "--no-install-menus "
    "--no-install-bin-symlink "
    "--no-install-hfs-symlink "
    "--no-install-license "
    "--no-install-hqueue-server "
    "--no-root-check "
    "--install-houdini "
    "--install-sidefxlabs "
    "--install-engine-maya "
    "--install-engine-unity "
    "--auto-install "
    "--make-dir "
    "{install_path}"
)


def commands():
    env.PYTHONPATH.prepend("{root}")
    env.PATH.prepend("{root}/bin")
