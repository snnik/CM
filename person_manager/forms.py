import datetime
from django import forms
from django.db.models import Max
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.forms import inlineformset_factory

from person_manager.models import Person, Card, Address, Terrain, DUL, SNILS, Polis


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
            self.fields['card_number'].widget.attrs['readonly'] = True
            self.fields['join_date'].widget.attrs['readonly'] = True
        else:
            self.fields['card_number'].initial = Card.objects.aggregate(Max('card_number'))['card_number__max'] + 1
            self.fields['join_date'].initial = datetime.date.today()


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('region', 'district', 'city', 'settlement',
                  'street', 'house', 'room', 'register_date', 'terrain_fk')
        widgets = {
            'city': forms.TextInput(attrs={'onclick': 'onChangeEventInput(this);', }),
            'settlement': forms.TextInput(attrs={'onclick': 'onChangeEventInput(this);', }),
            'register_date': forms.DateInput(attrs={'class': 'datepicker-here', 'required': False}),
            'terrain_fk': forms.Select(attrs={'onchange': 'onChangeEventSelect(this);', }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            if self.instance.terrain_fk == Terrain.objects.get(pk=1):
                self.fields['settlement'].widget.attrs['readonly'] = True
            if self.instance.terrain_fk == Terrain.objects.get(pk=2):
                self.fields['city'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('terrain_fk', css_class='col-12 col-lg-4 form-group'),
                Column('region', css_class='col-12 col-lg-4 form-group'),
                Column('district', css_class='col-12 col-lg-4 form-group'),
                css_class='form-row my-0'
            ),
            Row(
                Column('city', css_class='col-12 col-md-6 form-group'),
                Column('settlement', css_class='col-12 col-md-6 form-group'),
                css_class='form-row my-0'
            ),
            Row(
                Column('street', css_class='col-12 col-md-6 form-group'),
                Column('house', css_class='col-12 col-md-2 form-group'),
                Column('room', css_class='col-12 col-md-2 form-group'),
                Column('register_date', css_class='col-12 col-md-2 form-group'),
                css_class='form-row my-0'
            )
        )


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ['create_date', 'update_date', 'is_delete', 'user_id', 'card_fk']

        widgets = {
            'male_fk': forms.RadioSelect(attrs={'class': 'list-unstyled'}),
            'birthday': forms.DateInput(attrs={'class': 'datepicker-here'}),
            'phone': forms.TextInput(attrs={'class': 'phone'}),
            'phone_mobile': forms.TextInput(attrs={'class': 'phone'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['last_name'].widget.attrs['readonly'] = True
            self.fields['first_name'].widget.attrs['readonly'] = True
            self.fields['patronymic_name'].widget.attrs['readonly'] = True
            self.fields['male_fk'].widget.attrs['readonly'] = True
            self.fields['birthday'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('last_name', css_class='col-12 col-xl-3 form-group'),
                Column('first_name', css_class='col-12 col-xl-3 form-group'),
                Column('patronymic_name', css_class='col-12 col-xl-3 form-group'),
                Column('birthday', css_class='col-6 col-xl-2 form-group'),
                Column('male_fk', css_class='col-6 col-xl-1 form-group'),
            ),
            Row(
                Column('phone_mobile', css_class='col-12 col-lg-4 col-xl-4 form-group'),
                Column('phone', css_class='col-12 col-lg-4 col-xl-4 form-group'),
                Column('email', css_class='col-12 col-lg-4 col-xl-4 form-group'),
            ),
        )


class SNILSForm(forms.ModelForm):
    class Meta:
        model = SNILS
        fields = ['number', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Column('number', css_class='col-12 form-group'))


class PolisForm(forms.ModelForm):
    class Meta:
        model = Polis
        exclude = ['series', 'person_fk', 'is_delete']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                    Column('polis_type', css_class='col-12 col-lg-4 form-group'),
                    Column('number', css_class='col-12 col-lg-4 form-group'),
                    Column('smo_id', css_class='col-12 col-lg-4 form-group')
                )
            )


class DULForm(forms.ModelForm):

    class Meta:
        model = DUL
        exclude = ['person', ]

        widgets = {
            'type': forms.Select(),
            'issuing': forms.Textarea(attrs={'rows': '4'}),
            'issue_date': forms.DateInput(attrs={'class': 'datepicker-here'}),
            'issue_country': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column('type', css_class='col-12 col-lg-4 form-group'),
                        Column('series', css_class='col-12 col-lg-4 form-group'),
                        Column('number', css_class='col-12 col-lg-4 form-group'),
                    ),
                    Row(
                        Column('issue_date', css_class='col-12 col-lg-4 form-group'),
                        Column('issue_code', css_class='col-12 col-lg-4 form-group'),
                        Column('issue_country', css_class='col-12 col-lg-4 form-group'),
                    ),
                    css_class='col-8'
                ),
                Column(
                    Row(
                        Column('issuing', css_class='col-12 form-group')
                    ),
                    css_class='col-4'),
            ),
        )


AddressFormSet = inlineformset_factory(parent_model=Person, model=Address, form=AddressForm,
                                       fields=AddressForm.Meta.fields, extra=1, max_num=1, can_delete=False)

DULFormSet = inlineformset_factory(parent_model=Person, model=DUL, form=DULForm, exclude=DULForm.Meta.exclude,
                                   max_num=1, extra=1, can_delete=False)

PolisFormSet = inlineformset_factory(parent_model=Person, model=Polis, form=PolisForm, exclude=PolisForm.Meta.exclude,
                                     max_num=1, extra=1, can_delete=False)
