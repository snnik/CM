from django.conf import settings
from django.conf.urls.static import static
from person_manager import views, exports
from django.urls import path

urlpatterns = [
    path('person/create/', views.CreatePerson.as_view(), name='create_person'),
    path('person/delete/<int:pk>/', views.DeletePerson.as_view(), name='delete_person'),
    path('person/<int:pk>/', views.EditPerson.as_view(), name='edit_person'),
    path('person/table_list', views.PersonTable.as_view(), name='person_table_list'),
    path('person/csv', exports.export_csv, name='import_csv'),
    path('person/viewcontent/<int:pk>', views.PersonContent.as_view(), name='person_content'),
    path('', views.PersonsList.as_view(), name='persons_list'),
]
