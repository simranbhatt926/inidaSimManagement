from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(PlanType)
admin.site.register(PackAmount)
admin.site.register(PackValidity)

admin.site.register(PackCategory)

admin.site.register(IndiaFRCSimPack)

# admin.site.register(ImageUpload)

admin.site.register(IndiaSimConstants)
# Register your models here.
admin.site.register(State)
admin.site.register(City)
admin.site.register(AcceptedPinCode)