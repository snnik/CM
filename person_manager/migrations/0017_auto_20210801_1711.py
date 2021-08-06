# Generated by Django 3.2.5 on 2021-08-01 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('person_manager', '0016_auto_20210730_0735'),
    ]

    operations = [
        migrations.CreateModel(
            name='Polis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(blank=True, max_length=10, verbose_name='Серия полиса')),
                ('number', models.CharField(blank=True, max_length=16, verbose_name='Номер полиса')),
            ],
            options={
                'verbose_name': 'Полис',
                'verbose_name_plural': 'Полис',
            },
        ),
        migrations.CreateModel(
            name='PolisType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('code', models.CharField(blank=True, default='', max_length=255)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='oms_fk',
        ),
        migrations.RemoveField(
            model_name='person',
            name='user_id',
        ),
        migrations.AddField(
            model_name='person',
            name='user_created',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_person_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='person',
            name='user_updated',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_person_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, default='', help_text='Введите адрес электронной почты', max_length=254, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, default='', help_text='Введите номер домашнего телефона', max_length=16, verbose_name='Домашний телефон'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone_mobile',
            field=models.CharField(blank=True, default='', help_text='Введите номер мобильного телефона', max_length=16, verbose_name='Мобильный телефон'),
        ),
        migrations.RenameModel(
            old_name='HealthInsuranceCompany',
            new_name='SMO',
        ),
        migrations.DeleteModel(
            name='OMS',
        ),
        migrations.AddField(
            model_name='polis',
            name='polis_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person_manager.polistype', verbose_name='tип полиса'),
        ),
        migrations.AddField(
            model_name='polis',
            name='smo_id',
            field=models.ForeignKey(blank=True, default=-1, on_delete=django.db.models.deletion.CASCADE, to='person_manager.smo', verbose_name='Организация, выдавшая ОМС'),
        ),
        migrations.AddField(
            model_name='person',
            name='polis_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='person_manager.polis', verbose_name='Полис'),
        ),
    ]
