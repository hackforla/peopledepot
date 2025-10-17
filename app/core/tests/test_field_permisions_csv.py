import pytest
from django.apps import apps

from core.api.access_control import AccessControl

# Adjust this path if your CSV file is located elsewhere


@pytest.mark.django_db
def test_model_fields_match_permissions_csv():
    """
    Ensure the fields listed for each table in permissions.csv exactly match
    the fields on the corresponding Django model — no extra and none missing.
    """
    # --- 1. Parse CSV ---
    table_to_fields = {}

    for row in AccessControl._get_csv_field_permissions():
        table = row["table_name"]
        field = row["field_name"]
        if table not in table_to_fields:
            table_to_fields[table] = set()
        table_to_fields[table].add(field)

    # --- 2. Check each model ---
    errors = []
    for table_name, csv_fields in table_to_fields.items():
        try:
            model = apps.get_model(
                app_label="core", model_name=table_name
            )  # adjust app_label if needed
        except LookupError:
            errors.append(f"Model not found for table '{table_name}'")
            continue

        model_fields = {
            f.name
            for f in model._meta.get_fields()
            if not (f.many_to_many or f.one_to_many)
        }

        missing_in_csv = model_fields - csv_fields
        extra_in_csv = csv_fields - model_fields

        if missing_in_csv or extra_in_csv:
            errors.append(
                f"Table '{table_name}' mismatch:\n"
                f"  Missing in CSV: {sorted(missing_in_csv)}\n"
                f"  Extra in CSV: {sorted(extra_in_csv)}"
            )

    # --- 3. Assert all tables are consistent ---
    print("Errors:", errors)
    assert not errors, "\n\n".join(errors)
