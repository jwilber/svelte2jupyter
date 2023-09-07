import os.path as op
import shutil
import subprocess

from .constants import (
    CURRENT_DIR,
    LOCAL_COMPILED_DIR,
    LOCAL_COMPONENT_DIR,
    PROJECT_COMPONENT_DIR,
    PROJECT_DIR,
)


def get_component_js_script(name: str) -> str:
    """
    Retrieves the compiled JS script for a given component name.

    Parameters
    ----------
    name : str
        The name of the component.

    Returns
    -------
    str
        The JS script wrapped in a script tag.

    Raises
    ------
    Exception
        If the local component file does not exist.
    """
    # to do: add logic here:
    svelte_path = f"{name}.svelte"
    iife_path = f"{name}.iife.js"
    compiled_file = op.join(LOCAL_COMPILED_DIR, iife_path)
    components_file = op.join(LOCAL_COMPONENT_DIR, svelte_path)
    if not op.exists(compiled_file):
        print("Component not found, checking to see if it needs to be compiled.")
        # check if file is in local components, if yes, build it, otherwise, raise error
        if not op.exists(components_file):
            raise Exception(f"Could not find the local component '{svelte_path}' ")
        else:
            build_components(svelte_path)
    with open(compiled_file) as f:
        iife_path = f.read()
        return f"<script>{iife_path}</script>"


def file_exists(dir: str, file: str) -> bool:
    """
    Checks if a file exists in a given directory.

    Parameters
    ----------
    dir : str
        Directory path.
    file : str
        Name of the file.

    Returns
    -------
    bool
        True if file exists, otherwise False.
    """
    file_path = op.join(dir, file)
    if op.exists(file_path):
        return True
    else:
        return False


def get_svelte_props(name: str) -> list:
    """
    Retrieves the properties from a Svelte component file.

    Parameters
    ----------
    name : str
        The name of the Svelte component.

    Returns
    -------
    list
        A list of properties present in the component.
    """
    svelte_path = f"{name}.svelte"
    components_file = op.join(LOCAL_COMPONENT_DIR, svelte_path)
    props = []
    with open(components_file, "r") as f:
        for line in f:
            if "export let" in line:
                # Extract the prop name from the line
                prop = line.split(" ")[4]
                # Remove the semicolon from the end of the prop name
                if ";" in prop:
                    prop = prop[:-1]
                props.append(prop)
    return props


def build_components(component: str = None) -> None:
    """
    Rebuild components using vite.

    Parameters
    ----------
    component : str, optional
        The name of the component to rebuild. If not provided, all components will be rebuilt.
    """
    copy_components(LOCAL_COMPONENT_DIR, PROJECT_COMPONENT_DIR)
    # check that component exists, throw error if it doesnt
    if component is not None:
        if file_exists(PROJECT_COMPONENT_DIR, component):
            cli_cmd = f"cd {CURRENT_DIR} && rm -rf compiled && cd {PROJECT_DIR} && node buildComponents.js {component} && mv -f compiled {CURRENT_DIR}"
        else:
            raise Exception(f"Could not find {component} in {LOCAL_COMPONENT_DIR} ")
    else:
        cli_cmd = f"cd {CURRENT_DIR} && rm -rf compiled && cd {PROJECT_DIR} && node buildComponents.js && mv -f compiled {CURRENT_DIR}"
    # if it does, run below
    subprocess.run(
        cli_cmd,
        shell=True,
        cwd=PROJECT_DIR,
    )


def copy_components(localdir: str, projectdir: str) -> None:
    """
    Copy components from one directory to another.

    Parameters
    ----------
    localdir : str
        The source directory.
    projectdir : str
        The destination directory.
    """
    # make sure local directory exists
    if not op.isdir(localdir):
        raise Exception(f"Directory {localdir} does not exist.")
    else:
        # upload items from local static dir to project static dir
        if op.exists(projectdir):
            shutil.rmtree(projectdir)
            shutil.copytree(localdir, projectdir)
        else:
            shutil.copytree(localdir, projectdir)
