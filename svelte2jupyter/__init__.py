"""Module svelte2jupyter printing python version."""
from svelte2jupyter.npm_utils import (PROJECT_DIR, add_npm_dependency,
                                      build_components,
                                      check_if_node_modules_exists,
                                      init_npm_project)
from svelte2jupyter.package import package_component
from svelte2jupyter.render_component import render_component

# if node modules does notlocally, list a warning message to run npm init.
if not check_if_node_modules_exists():
    print(
        f"WARNING! It looks like the node project hasn't been set up yet in {PROJECT_DIR}.\n Running `init_npm_project` to set it up now:"
    )
    init_npm_project()
