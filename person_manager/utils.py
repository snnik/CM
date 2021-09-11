import datetime
import logging
from django.apps import apps
from django.db import transaction, IntegrityError, DatabaseError
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from person_manager.forms import CardForm, SNILSForm, AddressFormSet, PolisFormSet, DULFormSet

logger = logging.getLogger(__name__)


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = form.errors.get_json_data()
            return JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'uri': self.object.get_absolute_url(),
                'cname': 'address',
            }
            return JsonResponse(data)
        else:
            return response


def get_page_kwargs(*args, **kwargs):
    context = dict()
    context['patients'] = context['add_card'] = True
    context['container_wrapper'] = "container"
    context['page_title'] = 'Регистратура'
    return context


def get_create_person_kwargs(*args, **kwargs):
    context = dict()
    request = kwargs.get('request', None)
    person = kwargs.get('person', None)
    context.update(get_page_kwargs())
    if request.method == 'POST':
        context['card_form'] = CardForm(request.POST, instance=person.card_fk)
        context['AddressFormSet'] = AddressFormSet(request.POST, instance=person)
    else:
        context['AddressFormSet'] = AddressFormSet(instance=person)
        context['card_form'] = CardForm(instance=person.card_fk)
    return context


def get_update_person_kwargs(*args, **kwargs):
    context = dict()
    request = kwargs.get('request', None)
    person = kwargs.get('person', None)
    context.update(get_create_person_kwargs(request=request, person=person))
    if request.method == 'POST':
        context['snils_form'] = SNILSForm(request.POST)
        context['PolisFormSet'] = PolisFormSet(request.POST, instance=person)
        context['DULFormSet'] = DULFormSet(request.POST, instance=person)
    else:
        context['snils_form'] = SNILSForm(instance=person.snils_fk)
        context['PolisFormSet'] = PolisFormSet(instance=person)
        context['DULFormSet'] = DULFormSet(instance=person)
    return context


class PersonMixin:

    card_object = None

    def validation_o2o_form(self, form=None):
        if not form or form.has_changed():
            return
        if form.is_valid():
            object_form = form(commit=False)
            if hasattr(object_form, 'person') and not object_form.pk:
                object_form.person = self.object
            if hasattr(object_form, 'user_id'):
                object_form.pk = self.request.user.pk
            object_form.clean()
            object_form.save()
        else:
            raise ValidationError('Ошибка проверки формы')
        if isinstance(form, CardForm):
            self.card_object = object_form

    def validation_person_form(self, form):
        if not form.is_valid():
            form.add_error(None, form.errors)
            raise ValidationError('Ошибка проверки формы!')
        try:
            person = form.save(commit=False)
            if self.card_object:
                person.card_fk = self.card_object
            person.clean()
            person.save()
        except ValidationError as validation_error:
            raise ValidationError(validation_error)
        except DatabaseError as database_error:
            raise DatabaseError(database_error)
        messages.success(self.request, 'Пациент {person} создан.'
                         .format(person=str(person)), extra_tags='alert-success')

    def validation_formsets(self, formset=None):
        if not formset:
            return
        object_formset = formset(self.request.POST or None, self.request.FILES or None, instance=self.object)
        if object_formset.is_valid():
            object_formset.save()
        else:
            raise ValidationError('Ошибка проверки формы!')

    @transaction.atomic
    def validation_forms(self, form):

        try:
            logger.info('{d} Редактирвание пациента. Начало проведения транзакции. Пользователь: {u};'
                        .format(d=datetime.datetime.now(), u=str(self.request.user)))

            with transaction.atomic():
                if not self.object:
                    self.validation_o2o_form(CardForm)
                    messages.success(self.request, 'Карта {card} создана.'
                                     .format(card=self.card_object), extra_tags='alert-success')
                self.validation_person_form(form=form)
                self.validation_formsets(AddressFormSet)
                if self.object:
                    self.validation_formsets(PolisFormSet)
                    self.validation_formsets(DULFormSet)
                    self.validation_o2o_form(SNILSForm)
                    messages.success(self.request, 'Карта {card} обновлена.'
                                     .format(card=self.object.card_fk), extra_tags='alert-success')

        except DatabaseError as transaction_error:
            logger.error('{d} Ошибка при проведении транзакции: {e}'
                         .format(d=datetime.datetime.now(), e=str(transaction_error)))
        except ValidationError as validation_error:
            logger.error('{d} Ошибка валидации формы: {e}'
                         .format(d=datetime.datetime.now(), e=str(validation_error)))

        logger.info('{d}:Транзакция успешно завершена:Изменен объект-{i}:Пользователь:{u};'
                    .format(d=datetime.datetime.now(), i=str(self.object), u=str(self.request.user)))
