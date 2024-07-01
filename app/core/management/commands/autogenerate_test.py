import os
from django.apps import apps

from django.core.management.base import BaseCommand
from django.urls import reverse

from utils.utils import read_lines_and_close


class Command(BaseCommand):
    help = "Adds APIs to urls.py for a model"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("model_name", type=str)

    def handle(self, *__args__, **options):
        app_name = options["app_name"]
        model_name = options["model_name"]
        generate(app_name, model_name)


def generate(app_name, model_name):
    generate_conftest(app_name, model_name)
    generate_test(app_name, model_name)


def generate_conftest(app_name, model_name):
    print("Writing to conftest.py...")
    model = apps.get_model(app_name, model_name)

    verbose_name = model._meta.verbose_name
    function_name = verbose_name.replace(" ", "_").lower()

    # Complete file path
    file_path = os.path.join(os.getcwd(), f"{app_name}/tests/conftest.py")
    # Read existing content
    lines = read_lines_and_close(file_path)
    if any(model_name in line for line in lines):
        print(f"conftest.py already modified for {app_name}.{model_name}.")
        return 1
    import_added = False
    json_added = False
    fixture_added = False
    lines = read_lines_and_close(file_path)
    content = ""
    for line in lines:
        if "_json" in line and not json_added:
            json_added = True
            fields_text = get_fields_text(app_name, model_name)
            content += f"{function_name}_json = {{ {fields_text} }}\n"
        if "@pytest.fixture" in line and not fixture_added:
            fixture_added = True
            content += get_fixture_text(model_name, function_name)
        content += line
        if "models import" in line and not import_added:
            import_added = True
            import_position = line.find("import")
            new_line = line[:import_position] + f"import {model_name}\n"
            content += new_line


    with open(file_path, "w") as file:
        file.write(content)

    print("done")


def get_fields_text(app_name, model_name):
    model = apps.get_model(app_name, model_name)
    verbose_name = model._meta.verbose_name

    unique_fields = [
        field
        for field in model._meta.get_fields()
        if field.unique and not field.is_relation and not field.primary_key
    ]
    fields_text = ""
    for index, field in enumerate(unique_fields):
        if index > 0:
            fields_text += ", "
        fields_text += f'"{field.name}": "Test {field.name} {verbose_name}"'
    return fields_text


def get_fixture_text(model_name, function_name):
    return f"""@pytest.fixture
def {function_name}():
    return {model_name}.objects.create(**{function_name}_json)


"""


def generate_test(app_name, model_name):
    print("Writing to test_get_apis.py...")
    model = apps.get_model(app_name, model_name)
    verbose_name = model._meta.verbose_name
    verbose_with_underscore = verbose_name.replace(" ", "_").lower()
    verbose_with_dash = verbose_name.replace(" ", "-").lower()
    # Complete file path
    file_path = os.path.join(os.getcwd(), f"{app_name}/tests/test_api.py")
    # Read existing content

    lines = read_lines_and_close(file_path)
    if any(verbose_with_underscore in line for line in lines):
        print(f"test_get_apis.py already modified for {app_name}.{model_name}.")
        return 1
    unique_fields = [
        field
        for field in model._meta.get_fields()
        if field.unique and not field.is_relation and not field.primary_key
    ]
    asserts_text = ""
    for field in unique_fields:
        asserts_text += f'    assert response.json()[0]["{field.name}"] == {verbose_with_underscore}.{field.name}\n'
    url_added = False
    test_added = False
    test_text = f"""def test_{verbose_with_underscore}({verbose_with_underscore}):
    response = client.get({verbose_with_underscore.upper()}_URL)
{asserts_text}

   tes
"""
def test_create_<verbose_with_underscore>(auth_client, project, affiliate):
    payload = {
<field_list>
    }
    res = auth_client.post(AFFILIATION_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["is_sponsor"] == payload["is_sponsor"]
    assert res.data["is_partner"] == payload["is_partner"]
    assert res.data["affiliate"] == payload["affiliate"]
    assert res.data["project"] == payload["project"]

    with open(file_path, "w") as file:
        for line in lines:
            if "_URL =" in line and not url_added:
                url_added = True
                file.write(
                    f'{verbose_with_underscore.upper()}_URL = reverse("{verbose_with_dash}-list")\n'
                )
            if "def test" in line and not test_added:
                test_added = True
                file.write(test_text)
            file.write(line)

    print("done")
