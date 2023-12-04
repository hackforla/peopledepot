# Create initial data scripts

## Overview

The goal is to convert our initial data into scripts that can be loaded into the database when the backend is set up for the first time.

These are the steps:

1. Export the data into JSON
1. Generate a python script from the JSON data

### Prerequisites

You must have Docker installed

The initial data exists in a Google spreadsheet, such as [this one for People Depot][pd-data-spreadsheet]. There should be individual sheets named after the model names the data correspond to, such as `ProgramArea - Data`. The sheet name is useful for us to identify the model it corresponds to.

The sheet should be formatted like so:

- the first row contains the names of the field names in the model. The names must be exactly the same
- rows 2 to n are the initial data for the model we want to turn into a script.

## Convert the data into JSON

1. Export the data from the Google [spreadsheet][pd-data-spreadsheet]

    1. Find the sheet in the document containing the data to export. Let's use the `ProgramArea - Data` data as our example.
    1. Make sure that the first row (column names) is frozen. Otherwise, freeze it by selecting the first row in the sheet, then Menu > View > Freeze > Up to row 1
    1. Export to JSON. Menu > Export JSON > Export JSON for this sheet

1. Save the JSON into a file

    1. Select and copy all the JSON text
    1. Paste it into a new file and save it as [ModelNameInPascalCase]_export.json under app/core/initial_data/
    1. The Pascal case is important in the next step to generate a python script to insert the data. It must match the model's class name for this to work.

    **Potential data issue**
    There was a problem with the JSON exporter where it omitted the underscore in `occ_code`. It should be fixed now but it's good to pay attention to other column name problems and fix them in the [Google Apps script][apps-script] in the [spreadsheet][pd-data-spreadsheet]. You will find out when the data insertion fails if there's a problem.

## Convert JSON into Python script

1. Start Docker

1. From project root, run

    ```bash
    ./scripts/buildrun.sh
    ```

1. Go to the project root and run this command

    ```bash
    docker-compose exec web python scripts/convert.py core/initial_data/ProgramArea_export.json
    ```

1. Check that there's a new file called `app/core/scripts/programarea_seed.py` and that it looks correct

    1. You can run it to verify, but will need to remove that data if you care about restoring the database state

        1. Run this command to run the script

            ```bash
            docker-compose exec web python manage.py runscript programarea_seed
            ```

        1. To remove the data, go into the database and delete all rows from `core_programarea`

            ```bash
            docker-compose exec web python manage.py dbshell

            # now we have a shell to the db

            # see if all the seed data got inserted
            select count(*) from core_programarea;
            # shows 9 rows

            delete from core_programarea;
            # DELETE 9

            select count(*) from core_programarea;
            # shows 0 rows

            # ctrl-d to exit dbshell
            ```

## Combine Script in Migration

- Look for name of the last migration file in `core/data/migrations` directory

- Create a script in the same directory named `<number>_<model in lowercase>_seed.py` with the following contents and
    replace `<model in lower case>` and `<name of last script>` with appropriate values:

    ```py
    from django.db import migrations

    from core.models import <model in CamelCase>


    def run(__code__, __reverse_code__):
        <paste everything in seed script here>


    class Migration(migrations.Migration):
        initial = True
        dependencies = [("data", "<name of last script, or contents of max_migration.txt>")]

        operations = [migrations.RunPython(run, migrations.RunPython.noop)]
    ```

    For example:

    ```py
    from django.db import migrations

    from core.models import BookType


    def run(__code__, __reverse_code__):
        status = BookType(uuid=1, name="Example Book")
        status.save()


    class Migration(migrations.Migration):
        initial = True
        dependencies = [("data", "0011_author_seed")]

        operations = [migrations.RunPython(run, migrations.RunPython.noop)]
    ```

[apps-script]: https://thenewstack.io/how-to-convert-google-spreadsheet-to-json-formatted-text/#:~:text=To%20do%20this,%20click%20Extensions,save%20your%20work%20so%20far.
[pd-data-spreadsheet]: https://docs.google.com/spreadsheets/d/1x_zZ8JLS2hO-zG0jUocOJmX16jh-DF5dccrd_OEGNZ0/
