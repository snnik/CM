# Generated by Django 3.0.2 on 2020-03-27 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person_manager', '0004_person_passport_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='house',
            field=models.CharField(blank=True, max_length=10, verbose_name='Дом'),
        ),
        migrations.AlterField(
            model_name='address',
            name='room',
            field=models.CharField(blank=True, max_length=10, verbose_name='Квартира'),
        ),
        migrations.AlterField(
            model_name='address',
            name='terrain',
            field=models.CharField(choices=[('1', 'Городская'), ('2', 'Сельская')], default='1', max_length=1, verbose_name='Местность'),
        ),
    ]
