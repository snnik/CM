import locale
import datetime
import importlib
from person_manager import dog_template
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, TableStyle, Table, FrameBreak
from person_manager.models import Person

font_size = 8
pdfmetrics.registerFont(TTFont('Times', settings.REPORT_FONTS + 'Times New Roman_N.ttf'))
pdfmetrics.registerFont(TTFont('TimesBd', settings.REPORT_FONTS + 'Times New Roman_B.ttf'))
pdfmetrics.registerFont(TTFont('TimesIt', settings.REPORT_FONTS + 'Times New Roman_I.ttf'))
pdfmetrics.registerFont(TTFont('TimesBI', settings.REPORT_FONTS + 'Times New Roman_BI.ttf'))
registerFontFamily('Times', normal='Times', bold='TimesBd', italic='TimesIt', boldItalic='TimesBI')

header_style = ParagraphStyle('Body', fontName='Times', fontSize=font_size, leading=10, spaceBefore=6,
                              alignment=TA_CENTER)
header_style_right = ParagraphStyle('Body', fontName='Times', fontSize=font_size, leading=10, spaceBefore=6,
                                    alignment=TA_RIGHT)
header_style_left = ParagraphStyle('Body', fontName='Times', fontSize=font_size, leading=10, spaceBefore=6,
                                   alignment=TA_LEFT)
text_style = ParagraphStyle('Body', fontName='Times', fontSize=font_size, leading=10, spaceBefore=2,
                            alignment=TA_JUSTIFY)
list_style = ParagraphStyle('Body', fontName='Times', fontSize=font_size, leading=10, alignment=TA_JUSTIFY,
                            leftIndent=24)
footer_style = ParagraphStyle('Body', fontName='Times', fontSize=font_size, leading=10, spaceBefore=6, leftIndent=24)

contract = []


def format_data(pattern_text, template_data, data):
    data_dict = {}
    flag_string_find = False
    for item in template_data:
        pattern = '{' + str(item) + '}'
        if pattern in pattern_text:
            # TODO:составить шаблон, вставить в исходный текст
            flag_string_find = True
            string_value = template_data[item][0]
            string_length = int(len(pattern))
            template = '{' + str(item) + ':_<' + str(string_length) + '}'
            pattern_text = pattern_text.replace(pattern, template)
            # TODO:составить словарь с данными для подстановки
            data_dict[item] = string_value.format(**data)
        # if pattern in ['address_str1', 'address_str2', 'address_str3', 'address_str4']:

    if flag_string_find:
        result_string = pattern_text.format(**data_dict)
    else:
        result_string = pattern_text
    return result_string


def paragraph_append(flag, dict_date, dict_data):
    style = text_style
    if flag[0] == 'header':
        style = header_style
    elif flag[0] == 'list':
        style = list_style
    elif flag[0] == 'footer':
        style = footer_style
    elif flag[0] == 'annotation':
        style = header_style_right
    data = format_data(pattern_text=dict_date, template_data=dog_template.data_template, data=dict_data)
    result_object = Paragraph(data, style)
    return result_object


def table_append(flag, dict_date, dict_data):
    table_dict = dict_date
    for i in range(len(dict_date)):
        for j in range(len(dict_date[i])):
            data = format_data(pattern_text=dict_date[i][j], template_data=dog_template.data_template, data=dict_data)
            if i == 0 and (j == 0 or j == 1) and not flag[1] == 'tbl' and not flag[1] == 'city':
                table_data = Paragraph(data, header_style)
            elif i == 0 and j == 0 and flag[1] == 'city':
                table_data = Paragraph(data, header_style_left)
            elif i == 0 and j == 1 and flag[1] == 'city':
                table_data = Paragraph(data, header_style_right)
            else:
                table_data = Paragraph(data, text_style)
            table_dict[i][j] = table_data
    if flag[1] == 'tbl':
        tbl = Table(table_dict, [0.7 * cm, 6.5 * cm, 1.8 * cm, 2.5 * cm, 2.5 * cm])
        tbl.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Times', 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
            ('BOX', (0, 0), (-1, -1), 0.25, black),
            ('SPAN', (0, 7), (-1, -1))
        ]))
    else:
        tbl = Table(table_dict, len(table_dict) * [6.4 * cm], spaceBefore=3, spaceAfter=3)
        tbl.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Times', 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
    return tbl


def get_dict(id):
    const_age = settings.UNDERAGE
    d = datetime.datetime.now()
    result_dict = {}

    try:
        person = Person.objects.get(pk=id)
        result_dict['patient'] = str(person)
        result_dict['patient_short'] = '{f} {n}.{p}.'.format(f=str(person.last_name), n=str(person.first_name)[0:1],
                                                             p=str(person.patronymic_name)[0:1])

        result_dict['age'] = person.birthday
        card = person.card
        result_dict['card'] = card.card_number
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        result_dict['dog_date'] = d.strftime('"%d" %B %Y г.')
        
        if person.passport_series or person.passport_number:
            result_dict['passport_series'] = str(person.passport_series)
            result_dict['passport_number'] = str(person.passport_number)
            result_dict['passport_issuing'] = \
                '{issuer}, {issuer_code}'.format(issuer=str(person.passport_issuing),
                                                 issuer_code=str(person.passport_issue_code))
            result_dict['passport_issue_date'] = \
                '{d} {m} {y}'.format(d=person.passport_issue_date.strftime('"%d"'),
                                     m=person.passport_issue_date.strftime('%B'),
                                     y=person.passport_issue_date.strftime('%Y'))
        else:
            result_dict['passport_series'] = result_dict['passport_number'] = result_dict['passport_issuing'] = \
                result_dict['passport_issue_date'] = ''

        address = person.address_set.filter(type__type='REG').first()
        if address:
            result_dict['address'] = str(address)
        else:
            result_dict['address'] = ''

        result_dict['phone'] = str(person.phone_mobile)

    except ObjectDoesNotExist as e:
        print(str(e))
        result_dict = dict()
    return result_dict


def get_age(birthday):
    today = datetime.date.today()
    age = today.year - birthday.year
    if today.month < birthday.month:
        age -= 1
    elif today.month == birthday.month and today.day < birthday.day:
        age -= 1
    return age


def get_template(age):
    importlib.reload(dog_template)  # reload data module
    age = get_age(age)
    template = dict()
    if age > settings.UNDERAGE:
        template.update(dog_template.info_template)
        template.update(dog_template.contract_major_template)
    else:
        template.update(dog_template.info_template)
        template.update(dog_template.contract_minor_template)
    return template


def print_card(request, id):
    # Create the HttpResponse object with the appropriate PDF headers.
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', settings.REPORT_FONTS + 'arial.ttf'))
    pdfmetrics.registerFont(ttfonts.TTFont('Times New Roman', settings.REPORT_FONTS + 'Times New Roman.ttf'))
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="tstpdf.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=portrait(A4))
    p.drawImage(settings.DOC_TEMPLATES + 'CARD.png', 0, 0, 210*mm, 297*mm)
    p.setFont('Times New Roman', 11)
    person = Person()
    try:
        person = Person.objects.get(pk=id)
        card = person.card
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(405, 676, str(card.card_number))
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        p.drawString(312, 651, card.join_date.strftime('%B'))
        p.drawString(260, 651, str(card.join_date.day))
        p.drawString(420, 651, str(card.join_date.year))
        p.drawString(200, 637, person.last_name + ' ' + person.first_name
                     + ' ' + person.patronymic_name)
        p.drawString(390, 622, person.birthday.strftime('%B'))
        p.drawString(330, 622, str(person.birthday.day))
        p.drawString(500, 622, str(person.birthday.year))
        p.drawString(463, 579, person.phone_mobile)
        if person.male == "М":
            p.line(70, 620, 105, 620)
        if person.male == "Ж":
            p.line(110, 620, 147, 620)
        if person.snils_number:
            p.drawString(395, 554, person.snils_number if person.snils_number else '')
        p.drawString(105, 554, '')
        if person.oms_number:
            p.drawString(230, 554, person.oms_number if person.oms_number else '')
            p.drawString(290, 539, str(person.oms_insurance_company))
    except ObjectDoesNotExist as e:
        print(e)

    address = person.address_set.filter(type__type='REG').first()
    if address:
        p.drawString(320, 608, address.district)
        p.drawString(72, 594, '')  # район прописать
        p.drawString(235, 594, address.city)
        p.drawString(445, 594, address.locality)
        p.drawString(72, 579, address.street)
        p.drawString(310, 579, str(address.house))
        p.drawString(405, 579, str(address.room))
        if address.terrain == "1":
            p.line(95, 565, 153, 565)
        if address.terrain == "2":
            p.line(155, 565, 211, 565)

    # Льгота
    p.drawString(157, 523, '')
    p.drawString(280, 523, '')
    p.drawString(417, 523, '')
    p.drawString(487, 523, '')

    # Диагноз
    d = ''
    if d:
        p.drawString(110, 493, d[:100])  # Первая строка
        if len(d) > 100:
            p.drawString(50, 477, d[100:])  # Вторая строка
        p.drawString(70, 461, d)  # Доктор

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def print_contract_old(request, id):
    # Create the HttpResponse object with the appropriate PDF headers.
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', settings.REPORT_FONTS + 'arial.ttf'))
    pdfmetrics.registerFont(ttfonts.TTFont('Times New Roman', settings.REPORT_FONTS + 'Times New Roman.ttf'))
    response = HttpResponse(content_type='application/pdf')
    const_age = settings.UNDERAGE

    try:
        person = Person.objects.get(pk=id)
        age = get_age(person.birthday)
        if age > const_age:
            template_name_p1 = 'contract_adult_p1.png'
            template_name_p2 = 'contract_adult_p2.png'
        else:
            template_name_p1 = 'contract_not_adult_p1.png'
            template_name_p2 = 'contract_not_adult_p2.png'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response, pagesize=landscape(A4))
        p.drawImage(settings.DOC_TEMPLATES + template_name_p1, 0, 0, 297 * mm, 210 * mm)
        p.setFont('Times New Roman', 9)

        card = person.card
        p.drawString(640, 536, str(card.card_number))  # номер договора fix 10/04/2020
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        d = datetime.datetime.now()
        p.drawString(725, 503, d.strftime('"%d" %B %Y г.'))
        if age > const_age:
            p.drawString(440, 314, str(person))
            if len(str(person)) > 30:
                if len(person.last_name + ' ' + person.first_name) > 30:
                    p.drawString(253, 321, str(person.last_name))
                    p.drawString(225, 302, person.first_name + ' ' + person.patronymic_name)
                else:
                    p.drawString(253, 321, person.last_name + ' ' + person.first_name)
                    p.drawString(225, 302, person.patronymic_name)
            else:
                p.drawString(253, 321, str(person))
            address = person.address_set.filter(type__type='REG').first()
            if address:
                if len(str(address)) > 38:
                    p.drawString(250, 283, '{d},'.format(d=address.district))
                    p.drawString(225, 265, 'город {c},'.format(c=address.city))
                    p.drawString(225, 246, 'улица {s}, '.format(s=address.street))
                    p.drawString(225, 228, 'дом {h} {kv}'.format(kv=', квартира ' +
                                                                 str(address.room) if address.room else '',
                                                                 h=address.house))
                else:
                    p.drawString(250, 283, str(address))
            p.drawString(242, 208, str(person.phone_mobile))
            p.drawString(335, 97, '{f} {n}.{p}.'.format(f=str(person.last_name), n=str(person.first_name)[0:1],
                                                        p=str(person.patronymic_name)[0:1]))
        else:
            p.drawString(440, 275, str(person))

        p.showPage()

        p.drawImage(settings.DOC_TEMPLATES + template_name_p2, 0, 0, 297 * mm, 210 * mm)
        p.setFont('Times New Roman', 9)
        p.drawString(320, 532, str(d.strftime('"%d" %B %Y г.')))
        if age > const_age:
            p.drawString(162, 511, str(person))
            p.drawString(55, 490, str(card.card_number))
            p.drawString(60, 169, str(person))
            if person.passport_series or person.passport_number:
                p.drawString(140, 155, str(person.passport_series))
                p.drawString(220, 155, str(person.passport_number))
                p.drawString(90, 141, str(person.passport_issuing))
                p.drawString(60, 127, str(person.passport_issue_code))
                p.drawString(197, 127, person.passport_issue_date.strftime('"%d"'))
                p.drawString(227, 127, person.passport_issue_date.strftime('%B'))
                p.drawString(295, 127, person.passport_issue_date.strftime('%Y'))
        else:
            p.drawString(55, 490, str(card.card_number))
        p.showPage()
        p.save()
    except ObjectDoesNotExist as e:
        print(str(e))
    return response


def print_contract(request, id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    dict_data = get_dict(id)
    template_contract = get_template(dict_data['age'])

    doc = BaseDocTemplate(response, pagesize=landscape(A4))
    # Two Columns
    frame1 = Frame(doc.leftMargin - 2 * cm, doc.bottomMargin - 1 * cm, doc.width / 2 - 6 + 2 * cm,
                   doc.height + 2.5 * cm,
                   id='col1')
    frame2 = Frame(doc.leftMargin + doc.width / 2 + 6, doc.bottomMargin - 1 * cm, doc.width / 2 - 6 + 2 * cm,
                   doc.height + 2.5 * cm, id='col2')

    for key in template_contract:
        flag = key.split('_')
        if flag[0] == 'table':
            contract.append(table_append(flag, template_contract[key], dict_data))
        elif flag[0] == 'end':
            contract.append(FrameBreak())
        else:
            contract.append(paragraph_append(flag, template_contract[key], dict_data))
    doc.addPageTemplates(PageTemplate(id='TwoCol', frames=[frame1, frame2]))
    # build pdf stream
    doc.build(contract)
    return response

