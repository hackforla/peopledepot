# Generated by Django 4.0.10 on 2023-10-16 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_project_github_primary_url_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Language',
        ),
    ]
