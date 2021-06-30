from django.conf import settings
from django.conf.urls.static import static
from print_module import views
from django.urls import path

urlpatterns = [
    path('person/contract/<int:id>/', views.print_contract, name='print_contract'),
    path('person/date_select/<int:pk>/', views.RepresentView.as_view(), name='date_select_contract'),
    path('person/<int:id>/', views.print_card, name='print_card'),
]
