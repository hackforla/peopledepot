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
    print(f"Generating serializer for {app_name}.{model_name}")

    file_path = os.path.join(os.getcwd(), f"{app_name}/api/serializers.py")
    template_path = os.path.join(
        os.getcwd(), f"{app_name}/management/commands/serializer_template.txt"
    )

    content = read_file_and_close(file_path)
    if model_name in content:
        print(f"Serializer for {app_name}.{model_name} already exists.")
        return 1
    content = insert_model_text(app_name, model_name, content)

    serializer_content = read_file_and_close(template_path)
    serializer_content = get_serializer_text(app_name, model_name, serializer_content)

    with open(file_path, "w") as file:
        file.write(content + serializer_content)

    return 0


def insert_model_text(app_name, model_name, content):
    lines = content.split("\n")
    new_content = ""
    from_model_found = False

    for line in lines:
        print("line", line)
        new_content += line + "\n"
        if f"from {app_name}.models" in line and not from_model_found:
            from_model_found = True
            import_position = line.find("import")
            new_line = line[:import_position] + f"import {model_name}\n"
            new_content += new_line
    return new_content


def get_serializer_text(app_name, model_name, content):
    # set fields_text = list of fields in model
    model = apps.get_model(app_name, model_name)
    fields = [field.name for field in model._meta.get_fields() if not field.is_relation]

    fields_text = ""
    for index, field in enumerate(fields):
        if index > 0:
            fields_text += ", "
        fields_text += f'"{field}"'

    # set primary_key = primary key of model
    primary_key = model._meta.pk.name

    # replace {model_name}, {fields_text}, and {primary_key} in new_ending_text
    new_text = content.replace("{model_name}", model_name)
    new_text = new_text.replace("{fields_text}", fields_text)
    new_text = new_text.replace("{primary_key}", primary_key)
    return new_text
