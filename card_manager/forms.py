from django import forms
from .models import MedicalCard


class CardForm(forms.ModelForm):
    class Meta:
        model = MedicalCard
        fields = ('card_number', 'join_date', )
        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control form-control-danger date datepicker-here'}),
        }
