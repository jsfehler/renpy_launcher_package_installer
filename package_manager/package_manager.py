import os
import subprocess

import renpy


GAME_DIR = 'game'


def install_python_package(package_name, config):
    """Use pip to install an external python package into the current project.

    Arguments:
        package_name (str): The package to install. Equivalent to the
        first argument to "pip install"
        config (dict): Properties for the installer.
    """
    current_project = renpy.store.project.current

    target_dir = os.path.join(
        current_project.path,
        GAME_DIR,
        config['package_path'],
    )

    command = [
        config['executable_path'],
        "-m", "pip", "install",
        package_name, "--no-input", "--target={}".format(target_dir),
    ]

    output = "No output"

    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell=True,
        )

        packages = get_installed_packages(current_project)
        
        if package_name not in packages:
            req_file_path = os.path.join(current_project.path, "requirements.txt")
            
            with open(req_file_path, 'a') as f:
                f.write('{}\n'.format(package_name))

    except subprocess.CalledProcessError as exc:
        output = exc.output

    return output
    
    
def get_installed_packages(project):
    """Get a list of installed packages for the current project.
    
    Returns:
        list
    """    
    req_file_path = os.path.join(project.path, "requirements.txt")
    
    try:
        with open(req_file_path, 'r') as f:
            content = f.read()
            packages = content.split('\n')
    
    except IOError:
        packages = []
    
    return packages