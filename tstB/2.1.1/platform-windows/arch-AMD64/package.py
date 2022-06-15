name = "tstB"
version = "2.1.1"

requires = ["tstA-2.0.1+<2.1"]

variants = [["platform-windows", "arch-AMD64"]]

build_command = f"""
xcopy /E {{root}}\\bin {{install_path}}\\bin\\
"""

def pre_build_commands():
    import subprocess

    subprocess.run(["cmd", "/c", "mkdir", "bin"])
    subprocess.run(
        [
            "cmd",
            "/c",
            "echo",
            "echo Hello B",
            ">",
            "bin/tstB.bat"
        ]
    )


def commands():
    env.PATH.append("{root}/bin")