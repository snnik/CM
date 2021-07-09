import datetime
from django import forms
from django.db.models import Max
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from person_manager.models import Person, Card, Address


class SearchForm(forms.Form):
    search_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2'}), label=None)


class PaginatorForm(forms.Form):
    LITTLE = 10
    MIDDLE = 50
    LONG = 100
    ALL = 'ALL'
    list_count = ((LITTLE, '10'), (MIDDLE, '50'), (LONG, '100'), (ALL, 'Все'))
    list_field = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=list_count,
                                   initial=10, label=None)


class FilterForm(forms.Form):
    date_start = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control datepicker-here mr-sm-2'}),
                                 label=None, required=False)
    date_end = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control datepicker-here mr-sm-2'}),
                               label=None, required=False)


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ('card_number', 'join_date', )
        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control form-control-danger date datepicker-here'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['card_number'].disabled = True
            self.fields['join_date'].disabled = True
        else:
            self.fields['card_number'].initial = Card.objects.aggregate(Max('card_number'))['card_number__max'] + 1
            self.fields['join_date'].initial = datetime.date.today()


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('region', 'district', 'city', 'settlement',
                  'street', 'house', 'room', 'register_date', 'terrain')
        widgets = {
            'city': forms.TextInput(attrs={'onclick': 'onChangeEventInput(this);'}),
            'settlement': forms.TextInput(attrs={'onclick': 'onChangeEventInput(this);'}),
            'register_date': forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here',
                                                    'required': False}),
            'terrain': forms.Select(attrs={'onchange': 'onChangeEventSelect(this);'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.terrain == '1':
                self.fields['settlement'].widget.attrs['readonly'] = True
            if self.instance.terrain == '2':
                self.fields['city'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('terrain', css_class='col-12 col-md-4 col-lg-4 form-group my-0'),
                Column('region', css_class='col-12 col-lg-4 form-group'),
                Column('district', css_class='col-12 col-lg-4 form-group'),
                css_class='form-row my-0'
            ),
            Row(
                Column('city', css_class='col-12 col-lg-6 form-group'),
                Column('settlement', css_class='col-12 col-lg-6 form-group'),
                css_class='form-row my-0'
            ),
            Row(
                Column('street', css_class='col-12 col-lg-6 form-group'),
                Column('house', css_class='col-12 col-md-2 col-lg-2 form-group'),
                Column('room', css_class='col-12 col-md-2 col-lg-2 form-group'),
                Column('register_date', css_class='col-12 col-md-2 col-lg-2 form-group'),
                css_class='form-row my-0'
            )
        )


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ['create_date', 'update_date', 'is_delete', 'user_id', 'card']

        widgets = {
            'male': forms.RadioSelect(attrs={'class': 'list-unstyled'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-danger phone'}),
            'phone_mobile': forms.TextInput(attrs={'class': 'form-control form-control-danger phone'}),
            'passport_issuing': forms.Textarea(attrs={'class': 'form-control form-control-danger', 'rows': '4'}),
            'passport_issue_date': forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['last_name'].disabled = True
            self.fields['first_name'].disabled = True
            self.fields['patronymic_name'].disabled = True
            self.fields['male'].disabled = True
            self.fields['birthday'].disabled = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('last_name', css_class='col-12 col-xl-3 form-group'),
                Column('first_name', css_class='col-12 col-xl-3 form-group'),
                Column('patronymic_name', css_class='col-12 col-xl-3 form-group'),
                Column('birthday', css_class='col-6 col-xl-2 form-group'),
                Column('male', css_class='col-6 col-xl-1 form-group'),
            ),
            Row(
                Column('phone_mobile', css_class='col-12 col-lg-4 form-group'),
                Column('phone', css_class='col-12 col-lg-4 form-group'),
                Column('email', css_class='col-12 col-lg-4 form-group')
            ),
            Row(
                Column(
                    Row(
                        Column('passport_type', css_class='col-12 col-lg-4 form-group'),
                        Column('passport_series', css_class='col-12 col-lg-4 form-group'),
                        Column('passport_number', css_class='col-12 col-lg-4 form-group'),
                    ),
                    Row(
                        Column('passport_issue_date', css_class='col-12 col-lg-4 form-group'),
                        Column('passport_issue_code', css_class='col-12 col-lg-4 form-group'),
                        Column('passport_issue_country', css_class='col-12 col-lg-4 form-group'),
                    ),
                    css_class='col-8'
                ),
                Column(
                    Row(
                        Column('passport_issuing', css_class='col-12 form-group')
                    ),
                    css_class='col-4'),
            ),
            Row(
                Column('snils_number', css_class='col-12 col-lg-4 form-group'),
                Column('oms_number', css_class='col-12 col-lg-4 form-group'),
                Column('oms_insurance_company', css_class='col-12 col-lg-4 form-group')
            )
        )


class PersonAddressForm(forms.Form):
    card_number = forms.IntegerField()
    join_date = forms.DateField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    patronymic_name = forms.CharField()
    birthday = forms.DateField()
    email = forms.EmailField()
    phone = forms.CharField()
    phone_mobile = forms.CharField()
    male = forms.ChoiceField()
    passport_type = forms.ChoiceField()
    passport_series = forms.CharField()
    passport_number = forms.CharField()
    passport_issuing = forms.CharField()
    passport_issue_code = forms.CharField()
