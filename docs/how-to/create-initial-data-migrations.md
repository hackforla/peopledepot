# Create initial data scripts

## Overview

The goal is to convert our initial data into scripts that can be loaded into the database when the backend is set up for the first time.

These are the steps:

1. Export the data into a csv file
1. Generate a python script from the csv data

### Prerequisites

You must have Docker installed

The initial data exists in a Google spreadsheet, such as [this one for People Depot][pd-data-spreadsheet]. There should be individual sheets named after the model names the data correspond to, such as `ProgramArea - Data`. The sheet name is useful for us to identify the model it corresponds to.

The sheet should be formatted like so:

- the first row contains the names of the field names in the model. The names must be exactly the same
- rows 2 to n are the initial data for the model we want to turn into a script.

It is required that there be data in the first column of the sheet.

## Gather data for preparation

1. Export the data from the Google [spreadsheet][pd-data-spreadsheet]

    1. Find the sheet in the document containing the data to export. Let's use the `ProgramArea - Data` data as our example.
    1. Go to File -> Download -> Comma Separated Values (.csv). This will download the sheet as a .csv file.
    1. Copy the file to the app/core/initial_data directory.

## Convert data into Python script

1. Start Docker

1. From project root, run

    ```bash
    ./scripts/buildrun.sh
    ```

1. Go to the project root and run this command

    ```bash
    docker-compose exec web python scripts/convert.py "core/initial_data/PD_ Table and field explanations  - ProgramArea - Data.csv"
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

- Create a script in the same directory named `<number>_<modelnameinlowercase>_seed.py` with the following contents and
    replace `<model in lower case>` and `<name of last script>` with appropriate values:

    ```py
    from django.db import migrations

    from core.models import ModelNameInPascalCase


    def forward(__code__, __reverse_code__):
        # paste everything in seed script's run function here
        # remove pass below
        pass


    def reverse(__code__, __reverse_code__):
        ModelNameInPascalCase.objects.all().delete()


    class Migration(migrations.Migration):
        dependencies = [("data", "<name of last script, or contents of max_migration.txt>")]

        operations = [migrations.RunPython(forward, reverse)]
    ```

    For example:

    ```py
    from django.db import migrations

    from core.models import BookType


    def forward(__code__, __reverse_code__):
        items = [
            (1, "Hard Cover"),
            (2, "Soft Cover"),
        ]
        for uuid, name in items:
            BookType.objects.create(uuid=uuid, name=name)


    def reverse(__code__, __reverse_code__):
        BookType.objects.all().delete()


    class Migration(migrations.Migration):
        dependencies = [("data", "0011_author_seed")]

        operations = [migrations.RunPython(forward, reverse)]
    ```

[pd-data-spreadsheet]: https://docs.google.com/spreadsheets/d/1x_zZ8JLS2hO-zG0jUocOJmX16jh-DF5dccrd_OEGNZ0/
