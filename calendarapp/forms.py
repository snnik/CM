from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember
from django import forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-danger'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-danger', 'rows': '10'}),
            'start_time': forms.TextInput(attrs={'type': 'datetime-local',
                                         'class': 'form-control form-control-danger date datepicker-here',
                                         'data-timepicker': 'true'}),
            'end_time': forms.TextInput(attrs={'type': 'datetime-local',
                                       'class': 'form-control form-control-danger datepicker-here',
                                       'data-timepicker': 'true'}),
        }
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%d.%m.%Y %H:%M',)
        self.fields['end_time'].input_formats = ('%d.%m.%Y %H:%M',)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ['user']
