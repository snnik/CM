import datetime
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ContractForm(forms.Form):
    person_contract = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger', 'readonly': True}), label='ФИО Пациента', required=False)
    date_contract = forms.CharField(
        widget=forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here'}),
        label='Дата договора',
        initial=datetime.datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('person_contract', css_class='form-group col-md-6 mb-0'),
                Column('date_contract', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Продолжить', css_class='float-right btn-success'),
        )


class RepresentForm(forms.Form):
    MAN = 'М'
    WOMAN = 'Ж'
    MALE = ((MAN, 'Мужской'), (WOMAN, 'Женский'))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger'}), label='Фамилия')
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger'}), label='Имя')
    patronymic = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger'}), label='Отчество')
    male = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'list-unstyled'}), label='Пол',
                             choices=MALE, initial=MAN)
    birthday = forms.CharField(widget=forms.DateInput(
        attrs={'class': 'form-control form-control-danger datepicker-here'}), label='Дата рождения')
    phone_mobile = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger phone'}), label='Телефон')
    passport_series = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger'}), label='Серия')
    passport_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
                                      label='Номер')
    passport_issuing = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control form-control-danger', 'rows': '5'}), label='Выдан')
    passport_issue_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger'}), label='Код организации')
    passport_issue_date = forms.CharField(widget=forms.DateInput(
        attrs={'class': 'form-control form-control-danger datepicker-here'}), label='Дата выдачи')
    passport_issue_country = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-danger'}), label='Страна выдачи')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('patronymic', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('male', css_class='form-group col-md-4 mb-0'),
                Column('birthday', css_class='form-group col-md-4 mb-0'),
                Column('phone_mobile', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('passport_series', css_class='form-group col-md-2 mb-0'),
                Column('passport_number', css_class='form-group col-md-2 mb-0'),
                Column('passport_issue_date', css_class='form-group col-md-4 mb-0'),
                Column('passport_issue_country', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('passport_issuing', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Сохранить'),
        )
