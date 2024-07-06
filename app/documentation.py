import os

# Generate documentation
import pydoc

import django

# Set the environment variable for Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")

# Initialize Django
django.setup()

# Now you can safely import and use Django models and other components
import core.permission_util  # noqa: E402

pydoc.writedoc(core.permission_util)
