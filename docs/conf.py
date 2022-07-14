# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

# Need to build docs with Python 3.8 or higher for proper typing annotations, including from __future__ import annotations
assert sys.version_info.major == 3 and sys.version_info.minor >= 8

# Assign a build variable to the builtin module that inerts the @set_module decorator. This is done because set_module
# confuses Sphinx when parsing overloaded functions. When not building the documentation, the @set_module("galois")
# decorator works as intended.
import builtins
setattr(builtins, "__sphinx_build__", True)

import galois
import numpy


# -- Project information -----------------------------------------------------

project = "galois"
copyright = "2020-2022, Matt Hostetter"
author = "Matt Hostetter"
version = galois.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "sphinx_immaterial",
    "sphinx_immaterial.apidoc.python.apigen",
    "myst_parser",
    "sphinx_design",
    "sphinxcontrib.details.directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = [".rst", ".md", ".ipynb"]

# Tell sphinx that ReadTheDocs will create an index.rst file as the main file,
# not the default of contents.rst.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_immaterial"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "extra.css",
]

# Define a custom inline Python syntax highlighting literal
rst_prolog = """
.. role:: python(code)
   :language: python
   :class: highlight
"""

# Sets the default role of `content` to :python:`content`, which uses the custom Python syntax highlighting inline literal
default_role = "python"

html_title = "galois"
html_favicon = "../logo/galois-favicon-color.png"
html_logo = "../logo/galois-favicon-white.png"

# Sphinx Immaterial theme options
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
    },
    "site_url": "https://galois.readthedocs.io/",
    "repo_url": "https://github.com/mhostetter/galois",
    "repo_name": "mhostetter/galois",
    "repo_type": "github",
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/mhostetter/galois"
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/galois/"
        },
        {
            "icon": "fontawesome/brands/twitter",
            "link": "https://twitter.com/galois_py"
        },
    ],
    "edit_uri": "",
    "globaltoc_collapse": False,
    "features": [
        # "navigation.expand",
        "navigation.tabs",
        # "toc.integrate",
        # "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        "navigation.tracking",
        "toc.follow",
        "toc.sticky"
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "accent": "deep-orange",
            "toggle": {
                "icon": "material/weather-night",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "accent": "deep-orange",
            "toggle": {
                "icon": "material/weather-sunny",
                "name": "Switch to light mode",
            },
        },
    ],
    "analytics": {
        "provider": "google",
        "property": "G-4FW9NCNFZH"
    },
    # "font": {
    #     "code": "Ubuntu Mono"
    # },
    # "version_dropdown": True,
    # "version_info": [
    #     {
    #         "version": "https://sphinx-immaterial.rtfd.io",
    #         "title": "ReadTheDocs",
    #         "aliases": []
    #     },
    #     {
    #         "version": "https://jbms.github.io/sphinx-immaterial",
    #         "title": "Github Pages",
    #         "aliases": []
    #     },
    # ],
}

html_last_updated_fmt = ""
html_use_index = True
html_domain_indices = True


# -- Extension configuration -------------------------------------------------

# Create hyperlinks to other documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

autodoc_default_options = {
    "imported-members": True,
    "members": True,
    # "special-members": True,
    # "inherited-members": "ndarray",
    # "member-order": "groupwise",
}
autodoc_typehints = "signature"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"

autodoc_type_aliases = {
    "ElementLike": "~typing.ElementLike",
    "IterableLike": "~typing.IterableLike",
    "ArrayLike": "~typing.ArrayLike",
    "ShapeLike": "~typing.ShapeLike",
    "DTypeLike": "~typing.DTypeLike",
    "PolyLike": "~typing.PolyLike",
}

# Sphinx Immaterial API config
python_apigen_modules = {
    "galois": "api/galois.",
    "galois.typing": "api/galois.typing.",
}
python_type_aliases = autodoc_type_aliases
python_apigen_default_groups = [
    ("class:.*", "Classes"),
    ("data:.*", "Variables"),
    ("function:.*", "Functions"),
    ("method:.*", "Methods"),
    ("classmethod:.*", "Class methods"),
    ("property:.*", "Properties"),
    (r"method:.*\.[A-Z][A-Za-z,_]*", "Constructors"),
    (r"method:.*\.__[A-Za-z,_]*__", "Special methods"),
    (r"method:.*\.__(init|new)__", "Constructors"),
    (r"method:.*\.__(str|repr)__", "String representation"),
    (r"method:.*\.is_[a-z,_]*", "Tests"),
    (r"property:.*\.is_[a-z,_]*", "Tests"),
]
python_apigen_default_order = [
    ("class:.*", 10),
    ("data:.*", 11),
    ("function:.*", 12),
    ("method:.*", 24),
    ("classmethod:.*", 22),
    ("property:.*", 30),
    (r"method:.*\.[A-Z][A-Za-z,_]*", 20),
    (r"method:.*\.__[A-Za-z,_]*__", 23),
    (r"method:.*\.__(init|new)__", 20),
    (r"method:.*\.__(str|repr)__", 21),
    (r"method:.*\.is_[a-z,_]*", 31),
    (r"property:.*\.is_[a-z,_]*", 32),
]
python_apigen_order_tiebreaker = "alphabetical"
python_apigen_case_insensitive_filesystem = False
python_transform_type_annotations_pep585 = False
python_apigen_show_base_classes = True

ipython_execlines = ["import math", "import numpy as np", "import galois"]


# -- Monkey-patching ---------------------------------------------------------

SPECIAL_MEMBERS = [
    "__repr__", "__str__", "__int__",
    "__call__", "__len__", "__eq__",
]

def autodoc_skip_member(app, what, name, obj, skip, options):
    """
    Instruct autodoc to skip members that are inherited from np.ndarray.
    """
    if skip:
        # Continue skipping things Sphinx already wants to skip
        return skip

    if name == "__init__":
        return False
    elif hasattr(obj, "__objclass__"):
        # This is a NumPy method, don't include docs
        return True
    elif getattr(obj, "__qualname__", None) in ["FunctionMixin.dot", "Array.astype"]:
        # NumPy methods that were overridden, don't include docs
        return True
    elif hasattr(obj, "__qualname__") and getattr(obj, "__qualname__").split(".")[0] == "FieldArray" and hasattr(numpy.ndarray, name):
        if name in ["__repr__", "__str__"]:
            # Specifically allow these methods to be documented
            return False
        else:
            # This is a NumPy method that was overridden in one of our ndarray subclasses. Also don't include
            # these docs.
            return True

    if name in SPECIAL_MEMBERS:
        # Don't skip members in "special-members"
        return False

    if name[0] == "_":
        # For some reason we need to tell Sphinx to hide private members
        return True

    return skip


def autodoc_process_bases(app, name, obj, options, bases):
    """
    Remove private classes or mixin classes from documented class bases.
    """
    # Determine the bases to be removed
    remove_bases = []
    for base in bases:
        if base.__name__[0] == "_" or "Mixin" in base.__name__:
            remove_bases.append(base)

    # Remove from the bases list in-place
    for base in remove_bases:
        bases.remove(base)


# Only during Sphinx builds, monkey-patch the metaclass properties into this class as "class properties". In Python 3.9 and greater,
# class properties may be created using `@classmethod @property def foo(cls): return "bar"`. In earlier versions, they must be created
# in the metaclass, however Sphinx cannot find or document them. Adding this workaround allows Sphinx to document them.

def classproperty(obj):
    ret = classmethod(obj)
    ret.__doc__ = obj.__doc__
    return ret


ArrayMeta_properties = ["name", "characteristic", "degree", "order", "irreducible_poly", "primitive_element", "dtypes", "display_mode", "ufunc_mode", "ufunc_modes", "default_ufunc_mode"]
for p in ArrayMeta_properties:
    # Fetch the class properties from the private metaclasses
    ArrayMeta_property = getattr(galois._domains._array.ArrayMeta, p)

    # Temporarily delete the class properties from the private metaclasses
    delattr(galois._domains._array.ArrayMeta, p)

    # Add a Python 3.9 style class property to the public class
    setattr(galois.Array, p, classproperty(ArrayMeta_property))

    # Add back the class properties to the private metaclasses
    setattr(galois._domains._array.ArrayMeta, p, ArrayMeta_property)


FieldArrayMeta_properties = ["properties", "name", "characteristic", "degree", "order", "irreducible_poly", "is_primitive_poly", "primitive_element", "primitive_elements", "quadratic_residues", "quadratic_non_residues", "is_prime_field", "is_extension_field", "prime_subfield", "dtypes", "display_mode", "ufunc_mode", "ufunc_modes", "default_ufunc_mode"]
for p in FieldArrayMeta_properties:
    # Fetch the class properties from the private metaclasses
    if p in ArrayMeta_properties:
        ArrayMeta_property = getattr(galois._domains._array.ArrayMeta, p)
    FieldArrayMeta_property = getattr(galois._fields._array.FieldArrayMeta, p)

    # Temporarily delete the class properties from the private metaclasses
    if p in ArrayMeta_properties:
        delattr(galois._domains._array.ArrayMeta, p)
    delattr(galois._fields._array.FieldArrayMeta, p)

    # Add a Python 3.9 style class property to the public class
    setattr(galois.FieldArray, p, classproperty(FieldArrayMeta_property))

    # Add back the class properties to the private metaclasses
    if p in ArrayMeta_properties:
        setattr(galois._domains._array.ArrayMeta, p, ArrayMeta_property)
    setattr(galois._fields._array.FieldArrayMeta, p, FieldArrayMeta_property)


def setup(app):
    app.connect("autodoc-skip-member", autodoc_skip_member)
    app.connect("autodoc-process-bases", autodoc_process_bases)
