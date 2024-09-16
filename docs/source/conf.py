# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'IS2_Proyecto.settings'
import django
django.setup()


project = 'IS2_Proyecto'
copyright = '2024, Grupo07'
author = 'Grupo07'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_multiversion',
]

smv_branch_whitelist = r'^Ivan---based-on-cris$'  # Aca se especifica la rama que queres documentar, creo que pueden ser varios
smv_tag_whitelist = r'^Version-\d+\.\d+$'   #smv_tag_whitelist = r'^v\d+\.\d+$'  # Aquí se especifican las etiquetas de versión (por ejemplo, etiquetas como 'v1.0', 'v2.1'), en este caso Version-x.x

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
