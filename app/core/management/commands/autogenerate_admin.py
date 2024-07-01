import os
from django.core.management.base import BaseCommand

from utils.utils import read_lines_and_close


class Command(BaseCommand):
    help = "Adds code to admin.py for a model."

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("model_name", type=str)

    def handle(self, *__args__, **options):
        app_name = options["app_name"]
        model_name = options["model_name"]
        file_path = os.path.join(os.getcwd(), f"{app_name}/admin.py")
        generate(file_path, app_name, model_name)


def generate(file_path, app_name, model_name):
    print(f"Generating admin for {app_name}.{model_name}")
    lines = read_lines_and_close(file_path)

    # if the admin already exists, don't do anything
    if any(model_name in line for line in lines):
        print(f"Admin for {app_name}.{model_name} already exists.")
        return 1

    registered = False
    imported = False

    # add model_name before list of import
    # add admin.site.register(model_name) before the first admin.site.register
    with open(file_path, "w") as file:
        # Write lines up to the desired position
        for line in lines:
            if "admin.site.register" in line and not registered:
                registered = True
                file.write(f"admin.site.register({model_name})\n")

            file.write(line)

            if ".models import" in line and not imported:
                imported = True
                import_position = line.find("import")
                new_line = line[:import_position] + f"import {model_name}\n"
                file.write(new_line)

    print("Done")
