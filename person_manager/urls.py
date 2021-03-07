from django.conf import settings
from django.conf.urls.static import static
from person_manager import views, prints, exports
from django.urls import path

urlpatterns = [
    path('person/create/', views.CreatePerson.as_view(), name='create_person'),
    path('person/<int:pk>/', views.EditPerson.as_view(), name='edit_person'),
    path('person/print/contract/<int:id>/', prints.print_contract, name='print_contract'),
    path('person/print/<int:id>/', prints.print_card, name='print_card'),
    path('person/csv', exports.export_csv, name='import_csv'),
    path('person/viewcontent/<int:pk>', views.PersonContent.as_view(), name='person_content'),
    path('', views.PersonsList.as_view(), name='persons_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
