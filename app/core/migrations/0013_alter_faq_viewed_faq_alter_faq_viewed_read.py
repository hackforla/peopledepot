# Generated by Django 4.0.8 on 2022-10-31 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_faq_viewed_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq_viewed',
            name='faq',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.faq'),
        ),
        migrations.AlterField(
            model_name='faq_viewed',
            name='read',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Last read'),
        ),
    ]
