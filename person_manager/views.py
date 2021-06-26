from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.conf import settings
from person_manager.models import AddressType, Person
from person_manager.forms import CardForm, PaginatorForm, FilterForm, PersonForm, AddressForm
import logging
import datetime


logger = logging.getLogger(__name__)


# Create your views here.
class PersonsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    paginate_by = settings.PAGINATE
    permission_required = ('person_manager.view_person',)
    template_name = 'person_manager/persons_list.html'

    def get_context_data(self, **kwargs):
        kwargs['patients'] = True
        kwargs['patients_list'] = True
        kwargs['page_title'] = 'Список пациентов'
        kwargs['title'] = 'Список карт'
        kwargs['search_param'] = self.request.GET.get('search', '')
        kwargs['paginate_form'] = PaginatorForm()
        kwargs['filter_form'] = FilterForm()
        kwargs['container_wrapper'] = "container-fluid"
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        query_search = self.request.GET.get('search', None)
        queryset = Person.objects.filter(Q(is_delete=False)).\
            values('id', 'first_name', 'last_name', 'patronymic_name', 'card__join_date', 'card__card_number')
        if query_search:
            self.paginate_by = None
            queryset = queryset.filter(Q(last_name__contains=query_search) |
                                       Q(card__card_number__contains=query_search) |
                                       Q(phone__contains=query_search) |
                                       Q(phone_mobile__contains=query_search) |
                                       Q(snils_number__contains=query_search))
        return queryset.order_by('-card__join_date')


class PersonTable(PersonsList):
    template_name = 'person_manager/person_table.html'

    def get_queryset(self):
        queryset = Person.objects.all()
        return queryset


class PersonContent(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Person
    login_url = reverse_lazy('login')
    permission_required = ('person_manager.view_person', 'person_manager.view_address',
                           'person_manager.view_card')
    template_name = 'person_manager/components/person_detail_component.html'

    def get_context_data(self, **kwargs):
        kwargs['container_wrapper'] = "container"
        try:
            kwargs['address'] = self.object.address_set.get(type=AddressType.objects.get(type='REG'))
        except ObjectDoesNotExist:
            kwargs['address'] = ''
        if not self.object.snils_number:
            self.object.snils_number = ''
        if not self.object.oms_number:
            self.object.oms_number = ''
        if not self.object.passport_series:
            self.object.passport_series = ''
        if not self.object.passport_number:
            self.object.passport_number = ''
        return super().get_context_data(**kwargs)


class CreatePerson(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('persons_list')
    template_name = 'person_manager/person_form.html'
    permission_required = ('person_manager.add_person', 'person_manager.add_address', 'person_manager.view_addresstype',
                           'person_manager.add_card')

    def get_context_data(self, **kwargs):
        kwargs['address'] = AddressForm()
        kwargs['title'] = 'Добавить карту'
        kwargs['page_title'] = 'Список пациентов'
        kwargs['card'] = CardForm()
        kwargs['patients'] = True
        kwargs['add_card'] = True
        # kwargs['container_wrapper'] = "container-fluid"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        address_form = AddressForm(self.request.POST)
        card_form = CardForm(self.request.POST)
        if not form.is_valid():
            return self.form_invalid(form)
        try:
            with transaction.atomic():
                logger.info('{d} Создание пациента. Начало проведения транзакции. Пользователь: '
                            '{u}'.format(d=datetime.datetime.now(), u=str(self.request.user)))
                card = card_form.save(commit=False)
                card.clean()
                card.id_user = self.request.user.pk
                card.save()
                instance.card = card
                instance.clean()
                # instance.user_id = self.request.user.pk
                instance.save()
                if address_form.has_changed():
                    address = address_form.save(commit=False)
                    if address.city or address.settlement:
                        address.type = AddressType.objects.get(type='REG')
                        address.person = instance
                        address.clean()
                        address.save()
                messages.success(self.request, '{card} создана.'.format(card=card), extra_tags='alert-success')
        except Exception as e:
            logger.error('{d} Ошибка при проведении транзакции: {e}'.format(d=datetime.datetime.now(), e=str(e)))
            messages.error(self.request, 'Ошибка во время создания карты!' + str(e), extra_tags='alert-warning')
            return self.form_invalid(form)
        logger.info('{d} Транзакция успешно заевршена. Созданы объекты: {c}; {i}'
                    ';'.format(d=datetime.datetime.now(), c=str(card), i=str(instance)))
        return redirect(self.success_url)


class EditPerson(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = PersonForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('persons_list')
    permission_required = ('person_manager.change_person', 'person_manager.view_person', 'person_manager.add_address',
                           'perosn_manager.change_address', 'person_manager.view_address',
                           'person_manager.view_addresstype', 'person_manager.view_card', 'person_manager.add_card')

    def get_initial(self):
        super().get_initial()

    def get_context_data(self, **kwargs):
        kwargs['container_wrapper'] = "container"
        try:
            kwargs['address'] = \
                AddressForm(instance=self.object.address_set.get(type=AddressType.objects.get(type='REG')))
        except ObjectDoesNotExist:
            kwargs['address'] = AddressForm()
        kwargs['id'] = self.object.pk
        kwargs['title'] = 'Изменение карты'
        kwargs['page_title'] = 'Регистратура'
        kwargs['card'] = CardForm(instance=self.object.card)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            address_form = AddressForm(self.request.POST, instance=self.object.address_set.get())
        except ObjectDoesNotExist:
            address_form = AddressForm(self.request.POST)

        if not form.is_valid():
            form.add_error(None, form.errors)
            raise ValidationError("Ошибка валидации формы!")
        instance = form.save(commit=False)
        try:
            with transaction.atomic():
                instance.user_id = self.request.user
                logger.info('{d} Редактирвание пациента. Начало проведения транзакции. Пользователь: '
                            '{u}'.format(d=datetime.datetime.now(), u=str(self.request.user)))
                instance.clean()
                instance.save()
                if address_form.has_changed():
                    address = address_form.save(commit=False)
                    if address.city or address.settlement:
                        if not address_form.instance.pk:
                            address.type = AddressType.objects.get(type='REG')
                        address.person = instance
                        address.clean()
                        address.save()
                messages.success(self.request, 'Карта обновлена!', extra_tags='alert-success')
        except Exception as e:
            logger.error('{d} Ошибка при проведении транзакции: {e}'.format(d=datetime.datetime.now(), e=str(e)))
            messages.error(self.request, 'Ошибка во время обновления карты! ' + str(e), extra_tags='alert-warning')
            return self.form_invalid(form)
        logger.info('{d} Транзакция успешно заевршена. Изменен объект: {i}'
                    ';'.format(d=datetime.datetime.now(), i=str(instance)))
        return redirect(self.success_url)


class DeletePerson(LoginRequiredMixin, DeleteView):
    model = Person
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('persons_list')
    permission_required = ('person_manager.change_person', 'person_manager.view_person', 'person_manager.add_address',
                           'person_manager.change_address', 'person_manager.view_address',
                           'person_manager.view_addresstype', 'person_manager.view_card', 'person_manager.add_card',
                           'person_manager.delete_person')

    def get_context_data(self, **kwargs):
        kwargs['container_wrapper'] = "container"
        kwargs['id'] = self.object.pk
        kwargs['title'] = 'Удалить карту'
        kwargs['page_title'] = 'Регистратура'
        return super().get_context_data(**kwargs)
