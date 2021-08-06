from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from person_manager.mixins import PersonMixin
from person_manager.models import AddressType, Person
from person_manager.forms import PaginatorForm, FilterForm, PersonForm


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
            values('id', 'first_name', 'last_name', 'patronymic_name', 'card_fk__join_date', 'card_fk__card_number')
        if query_search:
            self.paginate_by = None
            queryset = queryset.filter(Q(last_name__contains=query_search) |
                                       Q(card_fk__card_number__contains=query_search) |
                                       Q(phone__contains=query_search) |
                                       Q(phone_mobile__contains=query_search) |
                                       Q(snils_fk__number__contains=query_search))
        return queryset.order_by('-card_fk__join_date')


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
        return super().get_context_data(**kwargs)


class CreatePerson(LoginRequiredMixin, PermissionRequiredMixin, CreateView, PersonMixin):
    model = Person
    form_class = PersonForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('persons_list')
    template_name = 'person_manager/person_form.html'
    permission_required = (
        'person_manager.add_person', 'person_manager.add_address', 'person_manager.add_card'
    )

    def get_context_data(self, **kwargs):
        person_context = self.get_person_data(context=super().get_context_data(**kwargs))
        person_context['title'] = 'Добавить карту'
        return dict(person_context)

    def form_valid(self, form):
        check = self.validation_forms(form=form)
        if check:
            return redirect(self.success_url)
        else:
            return self.form_invalid(form=form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, address=self.address_form,
                                                             card=self.card_form))


class EditPerson(LoginRequiredMixin, PermissionRequiredMixin, PersonMixin, UpdateView):
    model = Person
    form_class = PersonForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('persons_list')
    permission_required = (
        'person_manager.change_person', 'person_manager.add_address', 'person_manager.change_address'
    )

    def get_context_data(self, **kwargs):
        person_context = self.get_person_data(context=super().get_context_data(**kwargs))
        person_context['title'] = 'Изменение карты'
        return dict(person_context)

    def form_valid(self, form):
        check = self.validation_forms(form=form)
        if check:
            return redirect(self.success_url)
        else:
            return self.form_invalid(form=form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, address=self.address_form, card=self.card_form))


class DeletePerson(LoginRequiredMixin, DeleteView):
    model = Person
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('persons_list')
    permission_required = ('person_manager.delete_person',)

    def get_context_data(self, **kwargs):
        kwargs['container_wrapper'] = "container"
        kwargs['id'] = self.object.pk
        kwargs['title'] = 'Удалить карту'
        kwargs['page_title'] = 'Регистратура'
        return super().get_context_data(**kwargs)
