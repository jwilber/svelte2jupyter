import inspect
import json
from random import randint
from typing import Any, Dict

from .component_utils import build_components, get_component_js_script, get_svelte_props


class PackagedComponent:
    """Minimal, reusable, dependency-free representation of a component

    Parameters
    ----------
    name : str
        The name of the component.
    iife_script : str
        The script for the component.
    """

    def __init__(self, name: str, iife_script: str, div_id: str) -> None:
        """
        Initialize the component.
        """
        self.name = name
        self.iife_script = iife_script
        self.div_id = self.randomize_hash_id()
        # self.props = get_svelte_props(self.name)
        self.markup = ""

    def __repr__(self):
        return f"<PackagedComponent {self.name}>"

    @property
    def attributes(self) -> Dict[str, str]:
        """
        Return the attributes of the component.

        Returns
        -------
        Dict[str, Any]
            The component attributes.
        """
        return {
            "name": self.name,
            "iife_script": self.iife_script,
            "div_id": self.div_id,
            # "props": self.props,
            "markup": self.markup,
        }

    def add_params(self, params: Dict[str, Any]) -> None:
        """
        Add parameters to the component.

        Parameters
        ----------
        params : dict
            The parameters to add to the component.
        """
        js_data = json.dumps(params, indent=0)
        self.markup = f"""
        <div id="{self.div_id}"></div>
        <script>
        (() => {{
            var data = {js_data};
            window.{self.name}_data = data;
            var {self.name}_inst = new {self.name}({{
                "target": document.getElementById("{self.div_id}"),
                "props": data
            }});
        }})();
        </script>
        """

    # def get_svelte_props(self):
    #     return get_svelte_props(self.name)

    def rebuild_component(self) -> None:
        """
        Rebuild the class's underlying svelte component using vite.
        """
        # component needs to end in '.svelte'
        component = f"{self.name}.svelte"
        # rebuild component
        build_components(component)
        # make sure to update iife
        self.iife_script = get_component_js_script(self.name)

    def _repr_html_(self) -> str:
        """
        Return the component as an HTML string.
        """
        return f"""
        {self.iife_script}
        {self.markup}
        """

    def __call__(self, **kwargs: Any) -> "PackagedComponent":
        """
        Call the component with the given kwargs.

        Parameters
        ----------
        kwargs : any
            The kwargs to pass to the component.

        Returns
        -------
        PackagedComponent
            A python class representing the svelte component, renderable in Jupyter.
        """
        # render with given arguments
        self.add_params(kwargs)
        return self

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

    def save_to_file(self, file_path: str) -> None:
        """
        Create a reusable, dependency-free representation of the component python
        class and save it to a .py file.
        This containerized representation of the svelte component has no dependencies,
        so may then be easily added to any codebase.

        Parameters
        ----------
        file_path : str
            The path to the file. E.g. 'bar_chart.py'.
        """
        # Get the name of the class
        class_obj = self.__class__
        class_name = class_obj.__name__

        # Get the list of method names for the class
        method_names = [
            "__init__",
            "add_params",
            "randomize_hash_id",
            "_repr_html_",
            "__call__",
        ]

        # # Build the string representing the class definition
        class_def = "import json \n"
        class_def += "\nfrom random import randint\n"
        class_def += "\nfrom typing import Dict, Any \n\n"
        class_def += f"class {class_name}:\n"

        # Add the method definitions to the class definition string, skipping those in the skip list
        for method_name in method_names:
            method = getattr(self.__class__, method_name)
            method_def = inspect.getsource(method)
            class_def += f"{method_def}\n"

        # sub in actual values for class attributes and signature
        class_def = class_def.replace("self.name = name", f"self.name = '{self.name}'")
        class_def = class_def.replace(
            "self.iife_script = iife_script",
            f"""self.iife_script = '''{self.iife_script}'''""",
        )
        class_def = class_def.replace(
            "self.div_id = div_id", f"self.div_id = '{self.div_id}'"
        )
        class_def = class_def.replace(", name: str, iife_script: str, div_id: str", "")

        # # Write the class definition to a .py file
        with open(file_path, "w") as f:
            f.write(class_def)
