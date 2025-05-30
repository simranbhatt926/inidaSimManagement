# from django.contrib import admin

# # Register your models here.
# from .models import *


# admin.site.register(PlanType)
# admin.site.register(PackAmount)
# admin.site.register(PackValidity)

# admin.site.register(PackCategory)

# admin.site.register(IndiaFRCSimPack)

# # admin.site.register(ImageUpload)

# admin.site.register(IndiaSimConstants)
# # Register your models here.
# admin.site.register(State)
# admin.site.register(City)
# admin.site.register(AcceptedPinCode)
# # add
# admin.site.register(ConnectionType)

from django.contrib import admin
from .models import *
@admin.register(PlanType)
class PlanTypeAdmin(admin.ModelAdmin):
    list_display = ['plan_type', 'is_active']
    search_fields = ['plan_type']
    list_filter = ['is_active']

@admin.register(PackAmount)
class PackAmountAdmin(admin.ModelAdmin):
    list_display = ['pack_amount', 'is_active']
    search_fields = ['pack_amount']
    list_filter = ['is_active']

@admin.register(PackValidity)
class PackValidityAdmin(admin.ModelAdmin):
    list_display = ['pack_validity', 'is_active']
    search_fields = ['pack_validity']
    list_filter = ['is_active']

@admin.register(PackCategory)
class PackCategoryAdmin(admin.ModelAdmin):
    list_display = ['pack_category', 'is_active']
    search_fields = ['pack_category']
    list_filter = ['is_active']

@admin.register(IndiaFRCSimPack)
class IndiaFRCSimPackAdmin(admin.ModelAdmin):
    list_display = [
        'plan_description', 'operator', 'connection',
        'validity', 'amount', 'is_active',
        'traveller_plan', 'most_affordable'
    ]
    search_fields = ['plan_description', 'connection', 'operator__operator_name']
    list_filter = ['connection', 'validity', 'operator', 'is_active', 'traveller_plan', 'most_affordable']


@admin.register(IndiaSimConstants)
class IndiaSimConstantsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'created_at']
    search_fields = ['key']
    list_filter = ['key']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['state', 'is_active', 'iso_code']
    search_fields = ['state']
    list_filter = ['is_active']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city', 'state', 'is_active', 'is_cod']
    search_fields = ['city', 'state__state']
    list_filter = ['state', 'is_active', 'is_cod']

@admin.register(AcceptedPinCode)
class AcceptedPinCodeAdmin(admin.ModelAdmin):
    list_display = ['pin_code', 'is_active', 'is_cod', 'created_date']
    search_fields = ['pin_code']
    list_filter = ['is_active', 'is_cod']

@admin.register(ConnectionType)
class ConnectionTypeAdmin(admin.ModelAdmin):
    list_display = ['connection_type', 'is_active']
    search_fields = ['connection_type']
    list_filter = ['is_active']
