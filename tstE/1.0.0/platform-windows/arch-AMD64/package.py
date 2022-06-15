name = "tstE"
version = "1.0.0"

requires = ['tstD-1', 'tstC']

variants = [["platform-windows", "arch-AMD64"]]

build_command = f"""
xcopy /E {{root}}\\bin {{install_path}}\\bin\\
"""

def cook():
    print(f"Cooking {name}-{version} {variant}")
    print(f"root: {root}")
    print(f"build_path: {build_path}")
    print(f"install_path: {install_path}")
    import shutil, os
    shutil.copytree(os.path.join(root, "bin"), os.path.join(install_path, "bin"))

    

def pre_build_commands():
    import subprocess

    subprocess.run(["cmd", "/c", "mkdir", "bin"])
    subprocess.run(
        [
            "cmd",
            "/c",
            "echo",
            "echo Hello E",
            ">",
            "bin/tstE.bat"
        ]
    )


def commands():
    env.PATH.append("{root}/bin")
