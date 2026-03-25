## Description

This script works with the Django tables aucit spreadsheet: https://docs.google.com/spreadsheets/d/1G9kDheY3MdITZnrthTFIUyprrTEvlMYpkFYWbCAMCmA/

It creates a new sheet called `table-descriptions <date>` and populates it with the data from the spreadsheet.

## How to use

1. Open the spreadsheet
1. Copy the scripts
    1. Open the scripts project
        1. Open menu -> Extensions -> Apps Script
    1. Paste the contents of the scripts into files with the same names.
    1. Close the scripts project
1. Refresh the spreadsheet (F5)
    1. There should be a "CSV Tools" menu with an item "Upload CSV → New Sheet" to run the script
1. Run the script
    1. Click "Upload CSV → New Sheet"
    1. Select the CSV file
    1. Click "Import"
1. Check the results

## What it does

- Creates a new sheet called `table-descriptions <date>`
- Copies the data from the spreadsheet into the new sheet
    - Adds an extra table_name-prefix column which is what the Django Models are called
    - Adds 6 extra columns on the left for audit and helpers
- Applies formulas to the new sheet
    - generates Django app name from table_name
    - generates Django created Table from Django app name
    - generates table_name-prefix from table_name
    - generates Django created field from column_name
- Hides the helper columns
- Freezes the first row
- Colors the columns that came from the database
- Colors the rows that are manged by Django
- Applies a filter to the sheet: only show rows that are not defined by Django

## Column descriptions

- Audit columns:
    - `Fields audited`
    - `Change title of table`
    - `Audit`
- Helper columns:
    - `Django created Table` is whether this table is defined by Django (hidden in final sheet)
    - `Django created field` is whether this column is managed by Django
    - `Django app name` is the name of the Django app that defines this table (hidden in final sheet)
    - `table_name-prefix` is the name of the Django model that defines this table (replaces `table_name` in the final sheet)
- Columns from the CSV:
    - `table_name` is the name of the table in the database (hidden in final sheet)
    - `column_name` is the name of the column in the database
    - `data_type` is the type of the column in the database
    - `is_nullable` is whether the column is nullable in the database
