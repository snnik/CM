# Generated by Django 3.2.5 on 2021-07-17 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person_manager', '0008_auto_20210717_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='DUL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(max_length=5, verbose_name='Серия документа')),
                ('number', models.CharField(max_length=10, verbose_name='Номер документа')),
                ('issuing', models.TextField(blank=True, verbose_name='Кем выдан')),
                ('issue_code', models.CharField(blank=True, max_length=7, verbose_name='Код подразделения')),
                ('issue_date', models.DateField(blank=True, null=True, verbose_name='Дата выдачи')),
                ('issue_country', models.CharField(blank=True, default='Российская федерация', max_length=30, verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'ДУЛ',
                'verbose_name_plural': 'ДУЛ',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='oms',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='person_manager.oms', verbose_name='ОМС'),
        ),
        migrations.AddField(
            model_name='person',
            name='snils',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='person_manager.snils', verbose_name='СНИЛС'),
        ),
        migrations.RenameModel(
            old_name='DocumentType',
            new_name='DULType',
        ),
        migrations.DeleteModel(
            name='Passport',
        ),
        migrations.AddField(
            model_name='dul',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person_manager.person'),
        ),
        migrations.AddField(
            model_name='dul',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person_manager.dultype', verbose_name='Тип документа'),
        ),
        migrations.AlterUniqueTogether(
            name='dul',
            unique_together={('series', 'number')},
        ),
    ]