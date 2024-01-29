# converts an spreadsheet-exported json into one that can be used in a django
# migration

# example:
# docker-compose exec web python core/scripts/convert.py \
# core/initial_data/UserStatus_export.json

# to apply the seed script:
# docker-compose exec web python manage.py runscript userstatus-seed

import json
import sys
from pathlib import Path


def get_modelname(path):
    filename = Path(path).name
    return filename.split("_")[0]


def to_values_str(_input):
    values = []
    for key, value in _input.items():
        if key == "uuid" and isinstance(value, int):
            values.append(f"{value}")
        else:
            values.append(f'"{value}"')

    return ", ".join(values)


def to_keys_str(_input):
    values = []
    for key in _input.keys():
        values.append(f"{key}")

    return ", ".join(values)


def to_keys_indexes_str(_input):
    values = []
    for key in _input.keys():
        values.append(f"{key}={key}")

    return ", ".join(values)


def convert(file_path):
    with Path(file_path).open("r") as input_file:
        input_data = json.load(input_file)
        root = Path.cwd()
        model_name = get_modelname(file_path)

        output = f"from core.models import {model_name}\n\n"
        output += "def run():\n\n"
        output += "    items = [\n"
        for i in input_data:
            line = f"        ({to_values_str(i)}),\n"
            output += line
        output += "    ]\n"
        output += f"    for {to_keys_str(input_data[0])} in items:\n"
        output += f"        {model_name}.objects.create({to_keys_indexes_str(input_data[0])})\n"

        output_filename = model_name.lower() + "_seed.py"
        dst = root / "core/scripts" / output_filename
        with Path(dst).open("w") as outfile:
            outfile.write(output)


if __name__ == "__main__":
    try:
        arg = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input json file>")

    convert(arg)
# convert an spreadsheet-exported json into one that can be used in a django migration
# get path and read json file
# get model path
# write new json with model and fields

# example:
# docker-compose exec web python core/scripts/convert.py core/fixtures/userstatus_export.json
# to apply the seed script:
# docker-compose exec web python manage.py runscript userstatus-seed

import json
import sys
from pathlib import Path


def get_modelname(path):
    filename = Path(path).name
    return filename.split("_")[0]


def to_key_value(_input):
    # print(_input)
    values = []
    for key, value in _input.items():
        if key == "id":
            key = "id"
        if key == "uuid" and isinstance(value, int):
            values.append(f"{key}={value}")
        else:
            values.append(f'{key}="{value}"')

    # print(values)
    return ", ".join(values)


def convert(file_path):
    with Path(file_path).open("r") as input_file:
        input_data = json.load(input_file)
        # print(input_data)
        root = Path.cwd()
        # src = os.path.join(root, file_path)
        # print(src)
        model_name = get_modelname(file_path)

        output = f"from core.models import {model_name}\n\n"
        output += "def run(__state_apps__, __schema_editor__):\n\n"
        for i in input_data:
            values = to_key_value(i)
            line = f"    status = {model_name}({values})\n"
            line += "    status.save()\n"
            # print(line)
            output += line

        # print(output)

        output_filename = model_name.lower() + "_seed.py"
        # print(output_filename)
        dst = root / "core/scripts" / output_filename
        # print(dst)
        with Path(dst).open("w") as outfile:
            outfile.write(output)


if __name__ == "__main__":
    try:
        arg = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input json file>")
    # print(arg)

    convert(arg)
