# Generated by Django 3.2.2 on 2021-06-20 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person_manager', '0006_auto_20210620_0025'),
    ]

    operations = [

        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.CharField(blank=True, max_length=50, verbose_name='Область'),
        ),

        migrations.RenameField(
            model_name='address',
            old_name='district',
            new_name='region_new',
        ),

        migrations.RenameField(
            model_name='address',
            old_name='region',
            new_name='district',
        ),

        migrations.RenameField(
            model_name='address',
            old_name='region_new',
            new_name='region',
        ),
    ]
