import csv
from django.http import HttpResponse
from csv_export.views import CSVExportView
from person_manager.models import Person


class DataExportView(CSVExportView):
    model = Person
    fields = '__all__'


def export_csv(request):
    persons = Person.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list.csv"'
    writer = csv.writer(response, delimiter=';',)
    writer.writerow([
                     'Фамилия',
                     'Имя',
                     'Отчество',
                     'Дата рождения',
                     'Номер карты'
                    ])
    for person in persons:
        writer.writerow([
            str(person.first_name),
            str(person.last_name),
            str(person.patronymic_name),
            str(person.birthday),
            str(person.card)
        ])
    return response
