Sphinx
======

Overview
--------

Sphinx is a popular documentation generator for software projects, especially python projects.

Features
--------

Documentation versioning
   This will be useful when we have different stable and dev versions.
Easy to read
   It supports many themes, of which we're using the popular furo, which has a clean look and a dark mode.
Useful extensions
   There's a number of useful extensions that makes documentation easier to read.

See ADR for why we chose sphinx

.. todo:: link to the ADR page

How we use it
-------------

Local editing
^^^^^^^^^^^^^

#. Install the Tools

   .. code-block:: bash

      cd docs
      poetry install
      poetry shell

#. Run autobuild inside poetry shell

   .. code-block:: bash

      make livehtml

#. Open ``http://localhost:8000/`` to see the generated site
#. The page will auto-update when you save changes. If not, ``Ctrl-C`` the ``make livehtml`` command and re-run it.

Auto generate documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When changes are pushed onto github, it triggers a workflow to build and upload the resulting html documentation as github pages.

- github actions

References
----------

- `Sphinx reST syntax <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
- `MyST md syntax <https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html>`_
- `Furo <https://pradyunsg.me/furo/>`_
- `Sphinx-design <https://sphinx-design.readthedocs.io/en/furo-theme/>`_
