import csv
from django.http import HttpResponse
from person_manager.models import Person


def export_csv(request):
    persons = Person.objects.all();
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
