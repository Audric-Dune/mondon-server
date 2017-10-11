from cx_Freeze import setup, Executable

executables = [Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon/logo_get_speed.ico",
    targetName="Get speed3.exe"
    )]
include_files = ["icon", "objct"]
packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
        "include_files": include_files
    },
}

setup(
    name = "get_speed",
    options = options,
    version = "1.0",
    description = 'Enregistrement vitesse de la machine de production Mondon',
    executables = executables
)
