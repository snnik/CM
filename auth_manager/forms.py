from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from person_manager.models import Person, Card, Address, Terrain, DUL


class AuthForm(forms.Form):

    login = forms.CharField(
        widget=forms.TextInput(),
        label='Логин пользователя:'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Пароль:'
    )

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-auto align-self-center'
        self.helper.layout = Layout(
            Row(
                Column('login', css_class='col-12'),
                Column('password', css_class='col-12'),
                ),
            Row(
                Submit('save', 'Вход', css_class='btn btn-primary btn-icon')
            )

        )

