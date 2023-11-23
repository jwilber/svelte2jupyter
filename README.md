# svelte2jupyter

### Render Svelte Components in Jupyter Notebooks

svelte2jupyter is minimal Python library for rendering [Svelte](https://svelte.dev/) components in [Jupyter](https://jupyter.org/) notebooks:

- 30 second gif

## Installation

Install with pip:

```
pip install svelte2jupyter
```

## Basic Use

In the same directory as your notebook, create a `components/` directory and put any Svelte components you want inside of it. (Note, you don't need to worry about any npm stuff, it'll be handled behind the scenes).

E.g., your folder-structure should look something like:

```
├── Example.ipynb
└── components
    ├── BarChart.svelte
```

Then, in Python:

```py
import svelte2jupyter as sj
```

_Note: if it's your first time importing, svelte2jupyter will init the local node environment under the hood for you (in the location `sj.PROJECTDIR`)._

## Rendering Components in Jupyter

You can then render your components inside Jupyter via a functional or a class-based api:

```py
# render component from function api
sj.render_component('BarChart')

# render component from class api
barchart = sj.package_component(component='BarChart')
barchart()
```

(The name should just be whatever the component is saved as, without the `.svelte` extension.)

Component props can be passed directly in Python as arguments:

```py
# pass props into functional api
sj.render_component('BarChart', fill='coral', showXAxis=False)

# pass props into class-based api
barchart(fill='coral', showXAxis=False)
```


## Packaging Components into Reusable, Dependency-Free Python Code

In some cases, you may want a reusable class with the required visuals that you can pass around without any node dependencies. For example, maybe you author a machine learning library and want to add a new interactive data visualization function to that library, but you don't want to add additional dependencies for your users (e.g. you don't want it to be the case that users of your package have node.js or any other additional python (or JavaScript) dependencies.)

**svelte2jupyter provides you with a method to package your svelte components into a dependency-free python class that can be used anywhere**. Simply use the `save_to_file` method on a class component as follows:

```py
# render component from class api
barchart = sj.package_component(component='BarChart')

# create reusable, dependency .py file with code for class:
barchart.save_to_file('barchart_component.py')
```

The newly created `barchart_component.py` will be saved to your local directory. You can inspect the file for yourself and see a python class with, depending on the complexity of your Svelte component, some pretty crazy looking attributes (namely the `iife_script` attribute). But this is the only file you need! You can copy & paste it directly into a jupyter notebook or add it to a different code base without adding any new libraries or underlying node environment.


## npm dependencies

This project requires a local npm project setup in `sj.PROJECTDIR`. When you first import the package, it should be setup automatically, but you can also run this manually via `sj.init_npm_project()`.

If your component uses third-party npm dependencies, you may see an error when trying to render them. To fix this, you just have to install these dependencies directly to your project with the `add_npm_dependency` function:

```py
# add third-party npm dependencies to project
sj.add_npm_dependency('d3-shape', 'd3-array', 'd3-scale')
```

## Updating Svelte components

If you've updated your Svelte component and want to refresh it, you have two options:

1. Call the se the `build_component` function directly with the component's name as the argument
2. Call the `rebuild_component` method on the class instance of the component:

```py
# update component: function api
sj.build_component('BarChart')

# update component: class api (barchart instantiated previously)
barchart.rebuild_component()
```

If you want to create an `.iife.js` for every component in `components/`, you can use the `build_components` function without any arguments:

```py
# build all components
sj.build_components()
```

## How It Works

You'll notice, after rendering any component(s), that your local environment will update slightly: compiled versions of your component will be created in a local `compiled/` directory as follows:

```
├── Example.ipynb
└── components
    ├── BarChart.svelte
├── compiled
│   ├── BarChart.iife.js
```

## Alternatives

Several alternatives exist! The goal of `svelte2jupyter` is to be super easy to use: just move a component into a `components/` dir, render that component with one function call, and save it to a re-usable python class. 

However, alternatives exist with other benefits:

- pysvelte: pysvelte has a publishing system, for making articles from jupyter.
- anywidget: anywidget allows one to create ipythonwidgets from the components based on esm, which allows for bi-directional flow via traitlets (svelte2jupyter only allows python to pass data from python to javascript)
- cookiecutter templates: (e.g. ) (These seem to be deprecated in favor of anywidget).
