import pytest
def _parse_csv_permissions():
    table_to_fields = {}
    for row in AccessControl._get_csv_field_permissions():
        table = row["table_name"]
        field = row["field_name"]
        table_to_fields.setdefault(table, set()).add(field)
    return table_to_fields


def _compare_model_to_csv(table_name, csv_fields):
    try:
        model = apps.get_model(app_label="core", model_name=table_name)
    except LookupError:
        return [f"Model not found for table '{table_name}'"]

    model_fields = {
        f.name
        for f in model._meta.get_fields()
        if not (f.many_to_many or f.one_to_many)
    }
    missing_in_csv = model_fields - csv_fields
    extra_in_csv = csv_fields - model_fields

    if missing_in_csv or extra_in_csv:
        return [
            (
                f"Table '{table_name}' mismatch:\n"
                f"  Missing in CSV: {sorted(missing_in_csv)}\n"
                f"  Extra in CSV: {sorted(extra_in_csv)}"
            )
        ]
    return []


@pytest.mark.django_db
def test_model_fields_match_permissions_csv():
    table_to_fields = _parse_csv_permissions()
    errors = []
    for table_name, csv_fields in table_to_fields.items():
        errors.extend(_compare_model_to_csv(table_name, csv_fields))

    print("Errors:", errors)
    assert not errors, "\n\n".join(errors)
