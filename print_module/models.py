# import uuid
# from django.db import models
#
#
# class PrintTemplate(models.Model):
#
#     class Meta:
#         verbose_name = 'Настройки шаблона'
#         verbose_name_plural = verbose_name
#
#     OUTPUT_FORMAT = [
#         ('XML', 'xml-формат'),
#         ('PDF', 'Универсальный отчет PDF'),
#         ('CSV', 'Текстовый файл с раздилителями'),
#     ]
#
#     documents_template = models.CharField(verbose_name='Наименование шаблона')
#     code_template = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='Код шаблона')
#     xml_template = models.TextField(verbose_name='xml шаблон')
#     output_format = models.CharField(verbose_name='Формат выгрузки', max_length=3, choices=OUTPUT_FORMAT)
#     models_name = models.CharField(max_length=30, verbose_name='Таблицы')
#     models_field = models.CharField(verbose_name="Поля")
