"""For generating documentation for the core app

This script generates documentation based on pydoc comments in specified modules.
To see which documentation gets generated, see the pydoc.writedoc calls at
the bottom of the script.
"""

import os
import pydoc

import django

from core import field_permissions
from core import permission_util

# Set the environment variable for Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "peopledepot.settings")

# Initialize Django
django.setup()

# Now you can safely import and use Django models and other components

pydoc.writedoc(permission_util)
pydoc.writedoc(field_permissions)
