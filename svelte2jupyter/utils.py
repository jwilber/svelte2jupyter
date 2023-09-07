"""node utility functions"""
import os
import os.path as op
import shutil
import subprocess
from random import randint

from .constants import (CURRENT_DIR, LOCAL_COMPILED_DIR, LOCAL_COMPONENT_DIR,
                        PROJECT_COMPONENT_DIR, PROJECT_DIR)


def get_component_js_script(name):
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


def file_exists(dir, file):
    file_path = op.join(dir, file)
    if op.exists(file_path):
        return True
    else:
        return False


def get_svelte_props(name):
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


def check_if_node_modules_exists() -> bool:
    """
    Check if node_modules exists.
    """
    node_modules_path = op.join(PROJECT_DIR, "node_modules")
    # make sure local directory exists
    if not op.exists(node_modules_path):
        return False
    return True


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


def init_npm_project() -> None:
    """
    Initialize an npm project.
    """
    subprocess.run(
        f"npm install",
        shell=True,
        cwd=PROJECT_DIR,
    )


def add_npm_dependency(*deps: str) -> None:
    """
    Add npm dependency so that svelte may use it.

    e.g. if your component requires d3-array, you can call
        add_npm_dependency('d3-array')
    or, to add multiple,
        add_npm_dependency(['d3-array', 'd3-shape'])

    Parameters
    ----------
    deps : str
        The dependencies to add. Can be a single string or a list of strings.
    """
    if not all(isinstance(d, str) for d in deps):
        raise TypeError("Input should be a str or a list of str.")
    deps = " ".join(deps)
    subprocess.run(
        f"npm install {deps}",
        shell=True,
        cwd=PROJECT_DIR,
    )


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
            cli_cmd = f"cd {CURRENT_DIR}  && rm -rf compiled && cd {PROJECT_DIR} && node buildComponents.js {component} && mv -f compiled {CURRENT_DIR}"
        else:
            raise Exception(f"Could not find {component} in {LOCAL_COMPONENT_DIR} ")
    else:
        cli_cmd = f"cd {CURRENT_DIR}  && rm -rf compiled && cd {PROJECT_DIR} && node buildComponents.js && mv -f compiled {CURRENT_DIR}"
    # if it does, run below
    subprocess.run(
        cli_cmd,
        shell=True,
        cwd=PROJECT_DIR,
    )


def build_components_rm_compiled(component: str = None) -> None:
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


def randomize_hash_id(name: str) -> str:
    """
    Generate a random hash for div id for a component.

    Parameters
    ----------
    name : str
        The name of the component. E.g. 'BarChart'.

    Returns
    -------
    str
        The generated hash ID.
    """
    random_hex_id = hex(randint(10**8, 10**9))[2:]
    hashed_div_id = f"{name}-{random_hex_id}"
    return hashed_div_id
