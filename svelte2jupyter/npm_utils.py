"""node utility functions"""
import os.path as op
import subprocess

from .constants import PROJECT_DIR


def check_if_node_modules_exists() -> bool:
    """
    Check if node_modules exists.
    """
    node_modules_path = op.join(PROJECT_DIR, "node_modules")
    # make sure local directory exists
    if not op.exists(node_modules_path):
        return False
    return True


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
