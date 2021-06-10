from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
# TODO: Добавление физического лица как объекта без учета документов
# TODO: Выделить документы в отдельную сущность. Формат шаблона JSON, описание, GUID вместо кода
# TODO: field validation in document type objects
# TODO: conntacts: template validation


class Person(models.Model):

    class Meta:
        db_table = 'persons'
        verbose_name = 'Пациент'
        verbose_name_plural = verbose_name
        unique_together = [['passport_series', 'passport_number'], ]

    MAN = 'М'
    WOMAN = 'Ж'
    MALE = (
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
    )

    PASSPORT = 'PASSP'
    BIRTHDAY_DOCUMENT = 'BIRTH'
    DUL_TYPE = ((PASSPORT, 'Паспорт'),
                (BIRTHDAY_DOCUMENT, 'Свидетельство о рождении'))

    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic_name = models.CharField(max_length=30, verbose_name='Отчество')
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(help_text='Введите адрес электронной почты', verbose_name='Электронная почта', blank=True)
    phone = models.CharField(max_length=16, verbose_name='Домашний телефон',
                             help_text='Введите номер домашнего телефона', blank=True)
    phone_mobile = models.CharField(max_length=16, verbose_name='Мобильный телефон',
                                    help_text='Введите номер мобильного телефона', blank=True)
    male = models.CharField(max_length=1, choices=MALE, default=MAN, verbose_name='Пол')
    card = models.OneToOneField('person_manager.Card', on_delete=models.SET_NULL, null=True, verbose_name='Номер карты')
    passport_type = models.CharField(max_length=5, choices=DUL_TYPE, default=PASSPORT, verbose_name='Тип документа')
    passport_series = models.CharField(max_length=5, blank=True, null=True, verbose_name='Серия документа')
    passport_number = models.CharField(blank=True, max_length=10, null=True, verbose_name='Номер документа')
    passport_issuing = models.TextField(blank=True, verbose_name='Кем выдан')
    passport_issue_code = models.CharField(blank=True, verbose_name='Код подразделения', max_length=7)
    passport_issue_date = models.DateField(blank=True, null=True, verbose_name='Дата выдачи')
    passport_issue_country = models.CharField(max_length=30, blank=True, verbose_name='Страна',
                                              default='Российская федерация')
    snils_number = models.CharField(blank=True, null=True, unique=True, max_length=14, verbose_name='Номер СНИЛС')
    oms_number = models.CharField(blank=True, null=True, unique=True, max_length=16, verbose_name='Номер ОМС')
    oms_insurance_company = models.ForeignKey(to='person_manager.HealthInsuranceCompany',
                                              on_delete=models.CASCADE, verbose_name='Организация, выдавшая ОМС',
                                              blank=True, default=-1)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{f} {i} {o}'.format(f=self.last_name, i=self.first_name, o=self.patronymic_name)

    def get_absolute_url(self):
        return reverse('edit_person', args=[str(self.pk)])

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True

    def get_documents(self):
        documents = []
        if self.passport_number and self.passport_series:
            documents.append('Паспорт серия: {s} номер: {n}'.format(s=self.passport_series, n=self.passport_number))
        if self.snils_number:
            documents.append('СНИЛС номер: {n}'.format(n=self.snils_number))
        if self.oms_number:
            documents.append('ОМС номер: {n}'.format(n=self.oms_number))
        return documents

    def save(self, *args, **kwargs):
        if not self.passport_number:
            self.passport_number = None
        if not self.passport_series:
            self.passport_series = None
        if not self.oms_number:
            self.oms_number = None
        if not self.snils_number:
            self.snils_number = None
        self.last_name = str(self.last_name).strip().capitalize()
        self.first_name = str(self.first_name).strip().capitalize()
        self.patronymic_name = str(self.patronymic_name).strip().capitalize()
        super().save(*args, **kwargs)


class HealthInsuranceCompany(models.Model):
    class Meta:
        db_table = 'health_insurance_company'
        verbose_name = 'Страховая'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=255, verbose_name='Наименование')
    id_user = models.IntegerField(default=-1)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def delete(self, using=None, keep_parents=False):
        if self.pk == -1:
            pass
        else:
            super().delete(using=None, keep_parents=False)


class AddressType(models.Model):

    class Meta:
        db_table = 'address_type'
        verbose_name = 'Типы адресов'
        verbose_name_plural = verbose_name

    type = models.CharField(max_length=10, blank=False)
    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return "{name}".format(name=str(self.name))


class Address(models.Model):

    CITY = '1'
    COUNTRY = '2'
    terrain = (
        (CITY, 'Городская'),
        (COUNTRY, 'Сельская'),
    )

    class Meta:
        db_table = 'address'
        verbose_name = 'Адреса'
        verbose_name_plural = verbose_name

    type = models.ForeignKey('person_manager.AddressType', on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Тип адреса', help_text='Выберите тип адреса: Регистрация/Место пребывания')
    address_string = models.TextField(blank=True, verbose_name='Адрес строкой')
    district = models.CharField(max_length=50, blank=True, verbose_name='Регион')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    locality = models.CharField(max_length=50, blank=True, verbose_name='Населенный пункт')
    street = models.CharField(max_length=50, blank=True, verbose_name='Улица')
    house = models.CharField(blank=True, verbose_name='Дом', max_length=10)
    room = models.CharField(blank=True, verbose_name='Квартира', max_length=10)
    terrain = models.CharField(max_length=1, choices=terrain, default=CITY, verbose_name='Местность')
    register_date = models.DateField(blank=True, null=True, verbose_name='Дата регистрации')
    person = models.ForeignKey('person_manager.person', blank=True, null=True, on_delete=models.CASCADE)
    # район добавить

    def __str__(self):
        return "{name}".format(name=str(self.address_string))

    def is_registration_address(self):
        t = self.type
        if t.type == 'REG':
            return True
        else:
            return False

    def set_address_string(self):
        self.address_string = ''
        if self.district:
            self.address_string = '{d}, '.format(d=self.district)
        if self.city:
            self.address_string += 'г. {c}'.format(c=self.city)
        else:
            self.address_string += self.locality
        if self.street:
            self.address_string += ', ул. {s}'.format(s=self.street)
        if self.house:
            self.address_string += ', дом. {h}'.format(h=str(self.house))
        if self.room:
            self.address_string += ', кв. {r}'.format(r=str(self.room))

    def save(self, *args, **kwargs):
        self.set_address_string()
        return super(Address, self).save(*args, **kwargs)

    def clean_fields(self, exclude=None):
        super(Address, self).clean_fields()
        errors = {}
        try:
            if not self.city and not self.locality:
                raise ValidationError('Заполните поле "Город" или "Населенный пункт"!')
            if self.city and self.locality:
                raise ValidationError('Необходимо заполнить поле "Город" или "Населенный пункт"!')
        except ValidationError as e:
            errors['city'] = e.error_list
            errors['locality'] = e.error_list
        try:
            if self.terrain == '1':
                if not self.city:
                    raise ValidationError('Указана городская местность, но поле "Город" не заполнено!')
                if self.locality:
                    raise ValidationError('Для городской местности необходимо заполнить поле "Город"!')
        except ValidationError as e:
            errors['city'] = e.error_list
            errors['locality'] = e.error_list
        try:
            if self.terrain == '2':
                if not self.locality:
                    raise ValidationError('Указана сельская местность, но поле "Населенный пункт" не заполнено!')
                if self.city:
                    raise ValidationError('Для сельской местности необходимо заполнить поле "Населенный пункт"!')
        except ValidationError as e:
            errors['locality'] = e.error_list
            errors['city'] = e.error_list
        if errors:
            raise ValidationError(errors)


class Card(models.Model):

    class Meta:
        db_table = 'medical_card'
        verbose_name = 'Медицинская карта'
        verbose_name_plural = verbose_name

    card_number = models.IntegerField(unique=True)
    id_user = models.IntegerField(default=-1)
    join_date = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Карта №: {}'.format(str(self.card_number))
