import datetime
from django import forms
from django.db.models import Max
from .models import Person, Card, Address


class PersonViewForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['last_name', 'first_name', 'patronymic_name', 'male', 'birthday', 'phone', 'phone_mobile', 'email',]

        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control-plaintextform-control-danger', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control-plaintext form-control-danger', 'readonly': 'readonly'}),
            'patronymic_name': forms.TextInput(attrs={'class': 'form-control form-control-danger', 'readonly': 'readonly'}),
            'male': forms.RadioSelect(attrs={'class': 'list-unstyled', 'readonly': 'readonly'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control form-control-danger', 'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-danger phone', 'readonly': 'readonly'}),
            'phone_mobile': forms.TextInput(attrs={'class': 'form-control form-control-danger phone', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-danger', 'readonly': 'readonly'}),
        }


class SearchForm(forms.Form):
    search_field = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2'}),
                                   label=None,
                                   )


class PaginatorForm(forms.Form):
    LITTLE = 10
    MIDDLE = 50
    LONG = 100
    ALL = 'ALL'
    list_count = (
        (LITTLE, '10'),
        (MIDDLE, '50'),
        (LONG, '100'),
        (ALL, 'Все'))
    list_field = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                   choices=list_count,
                                   initial=10,
                                   label=None)


class FilterForm(forms.Form):
    date_start = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control datepicker-here mr-sm-2'}),
                                 label=None,
                                 required=False)
    date_end = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control datepicker-here mr-sm-2'}),
                               label=None,
                               required=False)


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ['create_date', 'update_date', 'is_delete', 'user_id', 'card']

        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'patronymic_name': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'male': forms.RadioSelect(attrs={'class': 'list-unstyled'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-danger phone'}),
            'phone_mobile': forms.TextInput(attrs={'class': 'form-control form-control-danger phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-danger'}),
            'passport_type': forms.Select(attrs={'class': 'form-control form-control-danger'}),
            'passport_series': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'passport_issuing': forms.Textarea(attrs={'class': 'form-control form-control-danger', 'rows': '5'}),
            'passport_issue_code': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'passport_issue_date': forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here'}),
            'passport_issue_country': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'snils_number': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'oms_number': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'oms_insurance_company': forms.Select(attrs={'class': 'form-control form-control-danger'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['last_name'].disabled = True
            self.fields['first_name'].disabled = True
            self.fields['patronymic_name'].disabled = True
            self.fields['male'].disabled = True
            self.fields['birthday'].disabled = True


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('region', 'district', 'city', 'settlement',
                  'street', 'house', 'room', 'register_date', 'terrain')
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'district': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-danger',
                                           'onclick': 'onChangeEventInput(this);'}),
            'settlement': forms.TextInput(attrs={'class': 'form-control form-control-danger',
                                               'onclick': 'onChangeEventInput(this);'}),
            'street': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'house': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'room': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'register_date': forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here',
                                                    'required': False}),
            'terrain': forms.Select(attrs={'class': 'form-control form-control-danger',
                                           'onchange': 'onChangeEventSelect(this);'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.terrain == '1':
                self.fields['settlement'].disabled = True
            if self.instance.terrain == '2':
                self.fields['city'].disabled = True


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ('card_number', 'join_date', )
        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control form-control-danger datepicker-here'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['card_number'].disabled = True
            self.fields['join_date'].disabled = True
        else:
            self.fields['card_number'].initial = Card.objects.aggregate(Max('card_number'))['card_number__max'] + 1
            self.fields['join_date'].initial = datetime.date.today()

# PersonFormSet = inlineformset_factory(Person, Address, )
