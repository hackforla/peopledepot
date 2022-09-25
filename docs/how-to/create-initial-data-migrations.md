# Create initial data migrations

## Overview

The goal is to convert our initial data into migration files so that they can be loaded into the database automatically

   1. Export the data into json
   1. Call convert.py to generate a script for the data
   1. Create a blank migration and call the initial data script from there
   1. Test the migration

## Convert the data into json

   1. Export the data from the spreadsheet
      1. Find the sheet in the document for the data to export. Let's use the `SOC Major` data as our example
      1. Make sure that the first row (column descriptions) is frozen. Otherwise, freeze it by selecting the first row in the sheet, Menu > View > Freeze > Up to row 1
      1. Export to JSON. Export JSON > Export JSON for this sheet
   1. Save the json into a file
      1. Select and copy all the json text
      1. Paste it into a new file and save it as [ModelNameInPascalCase]_export.json under app/core/initial_data/
      1. The Pascal case is important in the next step to generate a python script to insert the data
      1. **Potential problem**: In this case, there's a problem with the JSON exporter where it **omitted the underscore** in `occ_code`. We need to do a global replacement in the json file: s/occcode/occ_code/g

## Convert json into python

   1. Go to the project root and run this command

      ```bash
      docker-compose exec web python scripts/convert.py core/initial_data/SOCMajor_export.json
      ```

   1. Check that there's a new file called app/scripts/socmajor_seed.py and that it looks correct
      1. You can run it to verify, but will need to remove that data if you care about restoring the database state
         1. Run this command to run the script

            ```bash
            docker-compose exec web python manage.py runscript socmajor_seed
            ```

         1. To remove the data, go into the database and delete all from core_socmajor

            ```bash
            docker-compose exec web python manage.py dbshell

            # see if all the seed data got inserted
            select count(*) from core_socmajor;
            # shows 22 rows

            # now we're inside dbshell
            delete from core_socmajor;
            # DELETE 22

            # ctrl-d to exit dbshell
            ```

## Create the migration

   1. Create a blank migration file (for the core app, because all our models are in there)

      ```bash
      docker-compose exec web python manage.py makemigrations --empty core --name socmajor_initial_data
      ```

   1. Call our script from the migration file

      ```python
      from django.db import migrations


      def add_data(apps, schema_editor):
          from ..scripts import socmajor_seed

          socmajor_seed.run()


      def delete_data(apps, schema_editor):
          SOCMajor = apps.get_model("core", "SOCMajor")
          SOCMajor.objects.all().delete()


      class Migration(migrations.Migration):

          dependencies = [
              ("core", "0007_socmajor"),
          ]

          operations = [migrations.RunPython(add_data, delete_data)]
      ```

      1. We pass 2 arguments to RunPython: functions for forward and reverse migrations
      1. add_data calls the seed script
      1. delete_data empties the table

   1. Verify the migration works

      ```bash
      # apply the new migration
      docker-compose exec web python manage.py migrate core

      # reversing to a previous migration (best to go back just 1 from the current count)
      docker-compose exec web python manage.py migrate core 0004

      # forwarding to the latest migration
      docker-compose exec web python manage.py migrate core
      ```
