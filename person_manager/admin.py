from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Person)
admin.site.register(HealthInsuranceCompany)
admin.site.register(AddressType)
admin.site.register(Address)
admin.site.register(Card)
