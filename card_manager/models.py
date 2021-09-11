from django.db import models


class MedicalCard(models.Model):
    class Meta:
        verbose_name = 'Медицинская карта'
        verbose_name_plural = verbose_name

    card_number = models.IntegerField(unique=True, verbose_name='Номер')
    id_user = models.IntegerField(default=-1)
    join_date = models.DateField(verbose_name='Дата создания')

    def __str__(self):
        return 'Карта %s'.format(str(self.card_number))
