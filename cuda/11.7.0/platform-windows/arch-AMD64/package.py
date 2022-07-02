name = "cuda"
version = "11.7.0"


@early()
def variants():
    import os, ast
    variant = ast.literal_eval(os.getenv("REZ_COOK_VARIANT"))
    return [variant]


def commands():
    env.PATH.prepend("{root}/bin")
    env.CUDA_PATH = "{root}"
    env.CUDA_DIR = "{root}"
    env.CUDA_TOOLKIT_PATH = "{root}"
    env.CUDA_TOOLKIT_DIR = "{root}"
    env.CUDA_TOOLKIT_ROOT = "{root}"


build_command = """
echo 'Nothing to do'
"""

def pre_cook():
    import os

    fn = download(f"https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_516.01_windows.exe")
    print("")
    print("")
    print("================================================================================")
    print("={:^78s}=".format("WARNING"))
    print("=                                                                              =")
    print("= Cannot automatically install CUDA on Windows, please use the downloaded      =")
    print("= installer located at:                                                        =")
    print(f"={os.path.join(os.getcwd(), fn):^78s}=")
    print("= to install manually to the following path:                                   =")
    print(f"={install_path:^78s}=")
    print("=                                                                              =")
    print("================================================================================")
    print("")
    print("")


