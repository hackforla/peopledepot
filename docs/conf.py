# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "People Depot"
project_copyright = "2023, Civic Tech Structure"
author = ""
release = ""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.append(os.path.abspath("./_ext"))
extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx.ext.todo",
    "fix-sectnum",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "source_repository": "https://github.com/hackforla/peopledepot/",
    "source_branch": "main",
    "source_directory": "docs/",
}
html_title = f"{project}"

# -- MyST options

myst_heading_anchors = 3
myst_enable_extensions = ["colon_fence"]
myst_number_code_blocks = ["python"]

# -- sphinx.ext.todo options

# Uncomment below to see the todo notes
# todo_include_todos = True
# todo_link_only = True
