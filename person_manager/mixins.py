import datetime
import logging
from django.db import transaction
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from person_manager.forms import AddressForm, CardForm, DULForm
from person_manager.models import AddressType

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


class PersonMixin:
    forms_valid = False
    dul_form = DULForm
    address_form = AddressForm
    card_form = CardForm
    card_object = None
    address_object = None
    dul_object = None

    def get_instance(self, param=None):
        try:
            if not self.object:
                return None
            elif param == 'dul':
                return self.object.dul_set.get()
            elif param == 'address':
                return self.object.address_set.get(type=AddressType.objects.get(type='REG'))
            elif param == 'card':
                return self.object.card_fk
            else:
                return None
        except ObjectDoesNotExist as e:
            return None

    def get_person_data(self, **kwargs):
        context = kwargs['context']
        context['patients'] = context['add_card'] = True
        context['container_wrapper'] = "container"
        context['page_title'] = 'Регистратура'
        if self.object:
            context['id'] = self.object.pk
            if 'dul_form' not in context:
                context['dul_form'] = DULForm(instance=self.get_instance('dul'))
        if 'address' not in context:
            context['address'] = self.address_form(instance=self.get_instance('address'))
        if 'card' not in context:
            context['card'] = self.card_form(instance=self.get_instance('card'))
        return context

    def validation_fk_form(self, object_name=None):
        if not object_name:
            return

        object_form_name = '{name}_form'.format(name=object_name)
        object_fk_name = '{name}_object'.format(name=object_name)
        form = getattr(self, object_form_name)(
            self.request.POST,
            instance=self.get_instance(object_name)
        )
        setattr(self, object_form_name, form)

        if not form.has_changed():
            return
        if form.is_valid():
            setattr(self, object_fk_name, form.save(commit=False))
            object_fk = getattr(self, object_fk_name)
            if not object_fk.pk:
                setattr(object_fk, 'person', self.object)
            object_fk.clean()
            object_fk.save()
        else:
            setattr(self, object_form_name, form)
            raise ValidationError('Ошибка проверки формы')

    def validation_card_form(self):
        card_form = self.card_form(self.request.POST, instance=self.get_instance('card'))
        if not self.object:
            card_form = self.card_form(self.request.POST)
            self.card_object = card_form.save(commit=False)
            self.card_object.clean()
            self.card_object.id_user = self.request.user.pk
            try:
                self.card_object.save()
            except ValidationError as e:
                raise ValidationError(e)
            finally:
                self.card_form = card_form
        else:
            self.card_form = card_form

    def validation_person_form(self, form):
        if not form.is_valid():
            form.add_error(None, form.errors)
            raise ValidationError('Ошибка валидации формы!')
        try:
            person = form.save(commit=False)
            if self.card_object:
                person.card_fk = self.card_object
            person.clean()
            person.save()
        except ValidationError as e:
            raise ValidationError(e)

    def validation_forms(self, form):
        try:
            with transaction.atomic():
                logger.info(
                    '{d} Редактирвание пациента. Начало проведения транзакции. Пользователь: {u};'.format(
                        d=datetime.datetime.now(),
                        u=str(self.request.user)
                    ))
                if not self.object:
                    self.validation_card_form()
                self.validation_person_form(form=form)
                self.validation_fk_form('address')
                if self.object:
                    self.validation_fk_form('dul')
        except ValidationError as transaction_error:
            messages.error(self.request, 'Ошибка во время обновления карты: ' + str(transaction_error),
                           extra_tags='alert-warning')
            logger.error('{d} Ошибка при проведении транзакции: {e}'
                         .format(d=datetime.datetime.now(), e=str(transaction_error)))
            return False
        if self.card_object:
            messages.success(self.request, 'Карта {card} создана.'.format(card=self.card_object),
                             extra_tags='alert-success')
        else:
            messages.success(self.request, 'Карта {card} обновлена.'.format(card=self.object.card_fk),
                             extra_tags='alert-success')
        logger.info('{d}:Транзакция успешно завершена:Изменен объект-{i}:Пользователь:{u};'
                    .format(d=datetime.datetime.now(), i=str(self.object), u=str(self.request.user)))
        return True
