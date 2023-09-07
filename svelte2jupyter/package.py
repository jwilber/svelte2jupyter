from .component_utils import get_component_js_script
from .packaged_component import PackagedComponent
from .randomize_hash_id import randomize_hash_id


def package_component(component: str) -> "PackagedComponent":
    """
    Save class to a `PackagedComponent` object.
    This object is an object representation of the svelte component.
    Example:
        bar = sj.package_component("BarChart")
        bar(fill="red")
        bar.rebuild_components

    Parameters
    ----------
    component : str
        The name of the component.

    Returns
    -------
    PackagedComponent
        The packaged component.
    """
    iife_script = get_component_js_script(component)
    div_id = randomize_hash_id(component)
    return PackagedComponent(name=component, iife_script=iife_script, div_id=div_id)
