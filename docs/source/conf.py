# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

project = 'Bmi Calculator'
copyright = '2025, Tim Schuette, Domink Elias Hase'
author = 'Tim Schuette, Domink Elias Hase'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # Automatically generate documentation from docstrings
    'sphinx.ext.napoleon',       # For Google/NumPy style docstrings
    'sphinx_autodoc_typehints',  # Add type hints to docs
    'sphinx.ext.viewcode',       # Add links to source code
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
