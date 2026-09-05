from django.db import migrations, models
import django.db.models.deletion


def populate_modern_job_title(apps, schema_editor):
    UserEmploymentHistory = apps.get_model("core", "UserEmploymentHistory")
    ModernJobTitle = apps.get_model("core", "ModernJobTitle")

    for history in UserEmploymentHistory.objects.all():
        modern_job_title = ModernJobTitle.objects.filter(
            soc_detailed_id=history.soc_detailed_id,
            title=history.title,
        ).first()

        if modern_job_title is None:
            modern_job_title = ModernJobTitle.objects.create(
                soc_detailed_id=history.soc_detailed_id,
                title=history.title,
            )

        history.modern_job_title_id = modern_job_title.pk
        history.save(update_fields=["modern_job_title"])


class Migration(migrations.Migration):

    dependencies = [('core', '0062_permission_ended_permission_granted')]

    operations = [
        migrations.AddField(
            model_name="useremploymenthistory",
            name="modern_job_title",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_employment_histories",
                to="core.modernjobtitle",
            ),
        ),
        migrations.RunPython(
            populate_modern_job_title,
            migrations.RunPython.noop,
        ),
        migrations.RunSQL(
            "SET CONSTRAINTS ALL IMMEDIATE",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RemoveField(
            model_name="useremploymenthistory",
            name="soc_detailed",
        ),
        migrations.RemoveField(
            model_name="useremploymenthistory",
            name="title",
        ),
        migrations.AlterField(
            model_name="useremploymenthistory",
            name="modern_job_title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_employment_histories",
                to="core.modernjobtitle",
            ),
        ),
    ]
