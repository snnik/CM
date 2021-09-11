import datetime
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Male(models.Model):
    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = verbose_name
    name = models.CharField(max_length=20, verbose_name='Наименование')

    def __str__(self):
        return str(self.name)


class Terrain(models.Model):
    class Meta:
        verbose_name = 'Территория'
        verbose_name_plural = verbose_name
    name = models.CharField(max_length=20, verbose_name='Наименование')

    def __str__(self):
        return str(self.name)


class DULType(models.Model):
    class Meta:
        verbose_name = 'Тип ДУЛ'
        verbose_name_plural = verbose_name
    name = models.CharField(max_length=20, verbose_name='Тип документа')

    def __str__(self):
        return str(self.name)


class DUL(models.Model):
    class Meta:
        verbose_name = 'ДУЛ'
        verbose_name_plural = verbose_name
        unique_together = [['series', 'number'], ]

    type = models.ForeignKey('person_manager.DULType', verbose_name='Тип документа', on_delete=models.PROTECT, default=1)
    series = models.CharField(max_length=5, blank=True, default='', verbose_name='Серия документа')
    number = models.CharField(max_length=10, blank=True, default='', verbose_name='Номер документа')
    issuing = models.TextField(blank=True, verbose_name='Кем выдан')
    issue_code = models.CharField(blank=True, verbose_name='Код подразделения', max_length=7)
    issue_date = models.DateField(blank=True, null=True, verbose_name='Дата выдачи')
    issue_country = models.CharField(max_length=30, blank=True, verbose_name='Страна',
                                              default='Российская федерация')
    person = models.ForeignKey('person_manager.Person', on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)


    def __str__(self):
        return 'Документ {person}'.format(person=str(self.person))


class PolisType(models.Model):
    begin_date = models.DateField()
    end_date = models.DateField()
    code = models.CharField(max_length=255, default='', blank=True)
    name = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class Polis(models.Model):
    class Meta:
        verbose_name = 'Полис'
        verbose_name_plural = verbose_name
        unique_together = [['series', 'number'], ]

    polis_type = models.ForeignKey('PolisType', blank=True, on_delete=models.PROTECT,
                                   default=PolisType.objects.get(pk=-1), verbose_name='Тип полиса')
    series = models.CharField(blank=True, default='', max_length=10, verbose_name='Серия полиса')
    number = models.CharField(blank=True, default='', max_length=16, verbose_name='Номер полиса')
    smo_id = models.ForeignKey(to='person_manager.SMO', on_delete=models.CASCADE,
                               verbose_name='Страховая МО', blank=True, default=-1)
    person = models.ForeignKey('person_manager.Person', blank=True, null=True,
                               on_delete=models.CASCADE, verbose_name='Владелец полиса')
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return '{person} {polis_type}'.format(person=str(self.person_fk), polis_type=str(polis_type))


class SNILS(models.Model):
    class Meta:
        verbose_name = 'СНИЛС'
        verbose_name_plural = verbose_name
    number = models.CharField(blank=True, null=True, unique=True, max_length=14, verbose_name='Номер СНИЛС')
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return 'Полис {person}'.format(person=str(self.person), number=self.number)


class Person(models.Model):

    class Meta:
        db_table = 'persons'
        verbose_name = 'Пациент'
        verbose_name_plural = verbose_name

    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic_name = models.CharField(max_length=30, verbose_name='Отчество')
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(help_text='Введите адрес электронной почты', verbose_name='Электронная почта',
                              blank=True, default='')
    phone = models.CharField(max_length=16, verbose_name='Домашний телефон',
                             help_text='Введите номер домашнего телефона', blank=True, default='')
    phone_mobile = models.CharField(max_length=16, verbose_name='Мобильный телефон',
                                    help_text='Введите номер мобильного телефона', blank=True, default='')
    male_fk = models.ForeignKey('person_manager.Male', default=1, verbose_name='Пол', on_delete=models.CASCADE)
    card_fk = models.OneToOneField('person_manager.Card',  on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='Номер карты')
    snils_fk = models.OneToOneField('person_manager.SNILS', on_delete=models.CASCADE, blank=True,
                                 null=True, verbose_name='СНИЛС')
    person_fk = models.ForeignKey(to='self', on_delete=models.SET_NULL, verbose_name='Представитель',
                                  blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    user_created = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, blank=True,
                                     related_name='created_person_id')
    create_date = models.DateTimeField(auto_now_add=True)
    user_updated = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, blank=True,
                                     related_name='updated_person_id')
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{f} {i} {o}'.format(f=self.last_name, i=self.first_name, o=self.patronymic_name)

    def get_absolute_url(self):
        return reverse('edit_person', args=[str(self.pk)])

    def delete(self, *args, **kwargs):
        self.is_delete = True
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.last_name = str(self.last_name).strip().capitalize()
        self.first_name = str(self.first_name).strip().capitalize()
        self.patronymic_name = str(self.patronymic_name).strip().capitalize()
        super().save(*args, **kwargs)


class SMO(models.Model):
    class Meta:
        db_table = 'smo'
        verbose_name = 'Страховая'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=255, verbose_name='Наименование')

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if not self.pk == -1:
            super().delete(using=None, keep_parents=False)


class AddressType(models.Model):

    class Meta:
        db_table = 'address_type'
        verbose_name = 'Типы адресов'
        verbose_name_plural = verbose_name

    type = models.CharField(max_length=10, verbose_name='Тип')
    name = models.CharField(max_length=30, verbose_name='Наименование')

    def __str__(self):
        return "{name}".format(name=self.name)


class Address(models.Model):

    class Meta:
        db_table = 'address'
        verbose_name = 'Адреса'
        verbose_name_plural = verbose_name

    type = models.ForeignKey('person_manager.AddressType', on_delete=models.CASCADE,
                             default=AddressType.objects.get(type='REG').pk,verbose_name='Тип адреса',
                             help_text='Выберите тип адреса: Регистрация/Место пребывания')
    region = models.CharField(max_length=50, blank=True, verbose_name='Область')
    district = models.CharField(max_length=50, blank=True, verbose_name='Район')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    settlement = models.CharField(max_length=50, blank=True, verbose_name='Населенный пункт')
    street = models.CharField(max_length=50, blank=True, verbose_name='Улица')
    house = models.CharField(blank=True, verbose_name='Дом', max_length=10)
    room = models.CharField(blank=True, verbose_name='Квартира', max_length=10)
    terrain_fk = models.ForeignKey(to='person_manager.Terrain', verbose_name='Местность', default=1,
                                   on_delete=models.PROTECT)
    register_date = models.DateField(blank=True, null=True, verbose_name='Дата регистрации')
    person = models.ForeignKey('person_manager.person', blank=True, null=True, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        address_string = ''
        city = Terrain.objects.get(pk=1)
        settl = Terrain.objects.get(pk=2)

        if self.terrain_fk == city:
            if self.region:
                address_string = ', '.join([self.region, self.city])
            else:
                address_string = self.city

        if self.terrain_fk == settl:
            if self.region:
                address_string = self.region
                if self.district:
                    address_string = ', '.join([address_string, self.district, self.settlement])
                else:
                    address_string = ', '.join([address_string, self.settlement])
            elif self.district:
                address_string = ', '.join([self.district, self.settlement])
            else:
                address_string = self.settlement

        if self.street:
            address_string = ', '.join([address_string, self.street])
        if self.house:
            address_string = ', '.join([address_string, str(self.house)])
        if self.room:
            address_string = ', '.join([address_string, str(self.room)])
        return address_string

    def clean_fields(self, exclude=None):
        super(Address, self).clean_fields()
        city = Terrain.objects.get(pk=1)
        settl = Terrain.objects.get(pk=2)
        errors = {}
        try:
            if not self.city and not self.settlement:
                raise ValidationError('Заполните поле "Город" или "Населенный пункт"!')
            if self.city and self.settlement:
                raise ValidationError('Необходимо заполнить поле "Город" или "Населенный пункт"!')
        except ValidationError as e:
            errors['city'] = e.error_list
            errors['settlement'] = e.error_list
        try:
            if self.terrain_fk == city:
                if not self.city:
                    raise ValidationError('Указана городская местность, но поле "Город" не заполнено!')
        except ValidationError as e:
            errors['city'] = e.error_list
        try:
            if self.terrain_fk == settl:
                if not self.settlement:
                    raise ValidationError('Указана сельская местность, но поле "Населенный пункт" не заполнено!')
        except ValidationError as e:
            errors['settlement'] = e.error_list
        if errors:
            raise ValidationError(errors)


class Card(models.Model):

    class Meta:
        db_table = 'medical_card'
        verbose_name = 'Медицинская карта'
        verbose_name_plural = verbose_name

    card_number = models.IntegerField(unique=True, verbose_name='Номер')
    id_user = models.IntegerField(default=-1)
    join_date = models.DateField(verbose_name='Дата создания')

    def __str__(self):
        return 'Карта {}'.format(str(self.card_number))
