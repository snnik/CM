# Generated by Django 3.0.2 on 2020-02-01 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Типы адресов',
                'verbose_name_plural': 'Типы адресов',
                'db_table': 'address_type',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField(unique=True)),
                ('id_user', models.IntegerField(default=-1)),
                ('join_date', models.DateField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Медицинская карта',
                'verbose_name_plural': 'Медицинская карта',
                'db_table': 'medical_card',
            },
        ),
        migrations.CreateModel(
            name='HealthInsuranceCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('id_user', models.IntegerField(default=-1)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Страховая',
                'verbose_name_plural': 'Страховая',
                'db_table': 'health_insurance_company',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('patronymic_name', models.CharField(max_length=30, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('email', models.EmailField(blank=True, help_text='Введите адрес электронной почты', max_length=254, verbose_name='Электронная почта')),
                ('phone', models.CharField(blank=True, help_text='Введите номер домашнего телефона', max_length=16, verbose_name='Домашний телефон')),
                ('phone_mobile', models.CharField(blank=True, help_text='Введите номер мобильного телефона', max_length=16, verbose_name='Мобильный телефон')),
                ('male', models.CharField(choices=[('М', 'Мужской'), ('Ж', 'Женский')], default='М', max_length=1, verbose_name='Пол')),
                ('passport_series', models.CharField(blank=True, null=True, max_length=5, verbose_name='Серия документа')),
                ('passport_number', models.CharField(blank=True, null=True, max_length=10, verbose_name='Номер документа')),
                ('passport_issuing', models.TextField(blank=True, verbose_name='Кем выдан')),
                ('passport_issue_code', models.CharField(blank=True, max_length=7, verbose_name='Код подразделения')),
                ('passport_issue_date', models.DateField(blank=True, null=True, verbose_name='Дата выдачи')),
                ('passport_issue_country', models.CharField(blank=True, default='Российская федерация', max_length=30, verbose_name='Страна')),
                ('snils_number', models.CharField(blank=True, null=True, max_length=14, unique=True, verbose_name='Номер СНИЛС')),
                ('oms_number', models.CharField(blank=True, null=True, max_length=16, unique=True, verbose_name='Номер ОМС')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('user_id', models.IntegerField(default=-1)),
                ('card', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='person_manager.Card', verbose_name='Номер карты')),
                ('oms_insurance_company', models.ForeignKey(blank=True, default=-1, on_delete=django.db.models.deletion.CASCADE, to='person_manager.HealthInsuranceCompany', verbose_name='Организация, выдавшая ОМС')),
            ],
            options={
                'verbose_name': 'Пациент',
                'verbose_name_plural': 'Пациент',
                'db_table': 'persons',
                'unique_together': {('passport_series', 'passport_number')},
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_string', models.TextField(blank=True, verbose_name='Адрес строкой')),
                ('district', models.CharField(blank=True, max_length=50, verbose_name='Регион')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='Город')),
                ('locality', models.CharField(blank=True, max_length=50, verbose_name='Населенный пункт')),
                ('street', models.CharField(blank=True, max_length=50, verbose_name='Улица')),
                ('house', models.IntegerField(blank=True, null=True, verbose_name='Дом')),
                ('room', models.IntegerField(blank=True, null=True, verbose_name='Квартира')),
                ('terrain', models.CharField(choices=[('1', 'Городская'), ('2', 'Сельская')], default='1', help_text='Выберите местность: 1-Городская, 2-Сельская', max_length=1, verbose_name='Местность')),
                ('register_date', models.DateField(blank=True, null=True, verbose_name='Дата регистрации')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='person_manager.Person')),
                ('type', models.ForeignKey(blank=True, help_text='Выберите тип адреса: Регистрация/Место пребывания', null=True, on_delete=django.db.models.deletion.CASCADE, to='person_manager.AddressType', verbose_name='Тип адреса')),
            ],
            options={
                'verbose_name': 'Адреса',
                'verbose_name_plural': 'Адреса',
                'db_table': 'address',
            },
        ),
    ]