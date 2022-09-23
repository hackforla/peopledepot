# convert an spreadsheet-exported json into a script that can be used in a django migration
# get path and read json file
# get model path
# write new json with model and fields

import json

# example:
# docker-compose exec web python core/scripts/convert.py core/fixtures/userstatus_export.json
# to apply the seed script:
# docker-compose exec web python manage.py runscript userstatus-seed
import sys
from pathlib import Path


def get_modelname(path):
    """Extract model name from file path

    Assumes the name portion before the first underscore is the model name
    """
    filename = Path(path).name
    return filename.split("_")[0]


def to_key_eq_value_str(line):
    """Convert dictionary to string of key = value, separated by commas"""
    # print(line)
    values = []
    for key, value in line.items():
        values.append(f'{key}="{value}"')

    # print(values)
    return ", ".join(values)


def convert(file_path):
    """Convert valid a file of json objects into a python script which can insert the data into django

    file_path file is in a subdirectory of a django app. Suggested format is
    <appname>/initial_data/<ModelName>_export.json file_path ends in a filename
    in the format <ModelName>_export.json where the <ModelName> matches the one
    defined in the django project.

    The python script will be saved to <appname>/scripts/<modelname>_seed.py
    """
    json_file_path = Path(file_path)

    with json_file_path.open() as json_file:
        model_all = json.load(json_file)
        root = json_file_path.cwd()
        model_name = get_modelname(file_path)
        app_name = json_file_path.parents[1].name

        output = f"from core.models import {model_name}\n\n\n"
        output += "def run():\n\n"
        for model_dict in model_all:
            values = to_key_eq_value_str(model_dict)
            python_lines = f"    status = {model_name}({values})\n"
            python_lines += "    status.save()\n"
            # print(python_lines)
            output += python_lines

        # print(output)

        output_filename = model_name.lower() + "_seed.py"
        # print(output_filename)
        destination = Path(root) / app_name / "scripts" / output_filename
        # print(dst)
        with Path(destination).open(mode="w") as outfile:
            outfile.write(output)


if __name__ == "__main__":
    try:
        json_file_path = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <input json file>")
    # print(json_file_path)

    convert(json_file_path)
