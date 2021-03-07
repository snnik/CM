from django.urls import reverse_lazy
from person_manager.models import Address
from person_manager.forms import AddressForm
from django.views.generic import CreateView, UpdateView, ListView
from person_manager.mixins import AjaxableResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class RegisterAddress(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    model = Address
    form_class = AddressForm
    login_url = reverse_lazy('login')
    template_name = 'person_manager/ajax_address_form.html'


class EditAddress(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    model = Address
    form_class = AddressForm
    login_url = reverse_lazy('login')
    template_name = 'person_manager/ajax_address_form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class AjaxList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'person_manager/ajax_address_list_view.html'
    context_object_name = 'address'
    queryset = Address.objects.filter(id__in=[])