"""SvelteJupyterWidget."""
import json
from random import randint
from typing import Any, Dict

from .component_utils import get_component_js_script


class SvelteJupyterWidget:
    """Represents a Svelte component (ie. HTML/JS/CSS component) in Python."""

    def __init__(self, name: str, params: Dict[str, Any]):
        """Create a SvelteJupyterWidget from its name.
        This is the access point
        Name should correspond to a svelte component in `components/{name}.svelte`."""
        self.name = name
        self.iife_scripts = get_component_js_script(self.name)
        self.params = params
        self.markup = self.render_component(self.params)

    def __repr__(self):
        return f"<SvelteJupyterWidget {self.name}>"

    def render_component(self, params) -> str:
        # Create unique 'hashed' id for svelte div (svelte needs this for scope styles)
        random_id = hex(randint(10**8, 10**9))[2:]
        hashed_div_id = f"{self.name}-{random_id}"
        # params for component
        js_data = json.dumps(params, indent=0)
        html_str = f"""
        <div id="{hashed_div_id}"></div>
        <script>
        ( () => {{
            var data = {js_data};
            window.{self.name}_data = data;
            var {self.name}_inst = new {self.name}({{
                "target": document.getElementById("{hashed_div_id}"),
                "props": data
                }});
        }})();
        </script>
        """
        return html_str

    def _repr_html_(self):
        return f"""
        {self.iife_scripts}
        {self.markup}
        """
