import os
import pydoc
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "peopledepot.settings")
django.setup()
excluded_dirs = {"venv", "__pycache__", "migrations"}
excluded_files = {"settings.py", "wsgi.py", "asgi.py"}


def has_docstring(file_path):
    with Path.open(file_path, encoding="utf-8") as file:
        for line in file:
            if '"""' in line or "'''" in line:
                return True
    return False


def is_dir_excluded(dirname):
    for excluded_dir in excluded_dirs:
        if excluded_dir in dirname:
            return False
    return True


def get_dirs():
    root_dir = Path.cwd()
    dir_names = []
    for dirpath, __dirnames__, __filenames__ in os.walk(root_dir):
        if not is_dir_excluded(dirpath):
            continue
        relative_dir = os.path.relpath(dirpath, root_dir)
        dir_names.append(relative_dir)
    return dir_names


def is_file_included(filename):
    for exclude_file in excluded_files:
        if exclude_file in filename:
            return False
    return True


def get_files_in_directory(directory):
    files_in_dir = []
    for filename in os.listdir(directory):
        if not filename.endswith(".py"):
            continue

        if is_file_included(filename):
            files_in_dir.append(
                Path(directory, filename)
            )  # Path.join(directory, filename)
    return files_in_dir


def generate_pydoc():  # noqa: C901
    # Get directories to scan
    dirs = get_dirs()

    # Get all files within each directory
    files = []
    for dirname in dirs:
        files.extend(get_files_in_directory(dirname))

    # Print files being processed

    # Generate documentation for each file with a docstring
    for file_spec in files:
        if not has_docstring(file_spec):
            print(f"Skipping {file_spec} as it does not have a docstring.")
            continue

        # Convert file path to module name
        module_name = file_spec[:-3].replace(os.sep, ".")

        try:
            print(f"Generating documentation for {module_name}...")
            pydoc.writedoc(module_name)
        except Exception as e:
            print(f"Failed to generate documentation for {module_name}: {e}")


if __name__ == "__main__":
    generate_pydoc()
    print("Pydoc generation complete.")
