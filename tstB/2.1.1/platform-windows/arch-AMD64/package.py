name = "tstB"
version = "2.1.1"

requires = ["tstA-2.0.1+<2.1"]

variants = [["platform-windows", "arch-AMD64"]]

def cook():
    import os, shutil

    os.makedirs(f'{root}/bin', exist_ok=True)
    with open(f"{root}/bin/tstB.bat", "w") as f:
        f.write("cmd /C echo Hello B!")

    shutil.copytree(f"{root}/bin", f"{install_path}/bin")
    shutil.copyfile(f"{root}/package.py", f"{install_root}/package.py")


def commands():
    env.PATH.append("{root}/bin")