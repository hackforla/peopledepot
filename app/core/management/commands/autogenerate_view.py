import os
from django.apps import apps
from django.core.management.base import BaseCommand

from utils.utils import read_file_and_close, read_lines_and_close


class Command(BaseCommand):
    help = "Adds code to serializers.py to serialize a model."

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("model_name", type=str)

    def handle(self, *__args__, **options):
        app_name = options["app_name"]
        model_name = options["model_name"]
        generate(app_name, model_name)


def generate(app_name, model_name):
    print(f"Generating view for {app_name}.{model_name}")

    # get meta data verbose_name and verbose_name_plural
    model = apps.get_model(app_name, model_name)
    verbose_plural = model._meta.verbose_name_plural.__str__()
    verbose_name = model._meta.verbose_name.__str__()

    view_path = os.path.join(os.getcwd(), "core/management/commands/view_template.txt")
    end_text = read_file_and_close(view_path)
    end_text = end_text.replace("{model_name}", model_name)
    end_text = end_text.replace("{verbose_plural}", verbose_plural)
    end_text = end_text.replace("{verbose_name}", verbose_name)

    file_path = os.path.join(os.getcwd(), f"{app_name}/api/views.py")

    modified_content = ""
    lines = read_lines_and_close(file_path)
    models_added = False
    serializers_added = False
    for line in lines:
        modified_content += line
        if ".models" in line and not models_added:
            models_added = True
            import_position = line.find("import")
            new_line = line[:import_position] + f"import {model_name}\n"
            modified_content += new_line
        if ".serializers" in line and not serializers_added:
            serializers_added = True
            import_position = line.find("import")
            new_line = line[:import_position] + f"import {model_name}Serializer\n"
            modified_content += new_line

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write back the original content
        file.write(modified_content + end_text)

    print(f"View for {app_name}.{model_name} generated.")
