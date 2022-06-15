name = "tstA"
version = "2.0.1"

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
            "echo Hello A",
            ">",
            "bin/tstA.bat"
        ]
    )


def commands():
    env.PATH.append("{root}/bin")