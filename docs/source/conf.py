# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'harrison_functions'
copyright = '2019, Harrison Wang'
author = 'Harrison Wang'
version = '1.0'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    'sphinx.ext.autosummary',  # Create neat summary tables
    'rinoh.frontend.sphinx'
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary

# see: https://stackoverflow.com/questions/46263274/how-can-i-prevent-sphinx-from-displaying-the-full-path-to-my-class/66459610#66459610
# add_module_names = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'figure_align': 'http'
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# See: https://knowyourtoolset.com/2018/02/controlling-the-width-of-a-table-with-read-the-docs/
def setup(app):
   app.add_css_file('css/custom.css')

html_sidebars = {
    '**': [  'about.html',
             # 'localtoc.html',  # redundant to navigation
             'navigation.html',
             'searchbox.html',
        ]
}

autodoc_default_options = {"members": None}