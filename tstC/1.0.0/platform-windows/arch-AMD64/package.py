name = "tstC"
version = "1.0.0"

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
            "echo Hello C",
            ">",
            "bin/tstC.bat"
        ]
    )


def commands():
    env.PATH.append("{root}/bin")