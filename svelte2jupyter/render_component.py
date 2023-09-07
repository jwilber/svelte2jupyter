"""render_component."""
from .svelte_jupyter_widget import SvelteJupyterWidget


def render_component(component_name: str, **params) -> "SvelteJupyterWidget":
    """
    Render a Svelte component in a Jupyter notebook.

    Parameters
    ----------
    component_name : str
        The name of the Svelte component to render. E.g. "BarChart".
    params : keyword arguments
        Keyword parameters and arguments for the svelte component.
        E.g. fill="coral", showAxes=False.

    Returns
    -------
    SvelteJupyterWidget
        An instance of the `SvelteJupyterWidget` class, representing the rendered component
        with the given arguments.
    """
    return SvelteJupyterWidget(name=component_name, params=params)
