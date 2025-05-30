from django.contrib import admin
from .models import *
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'mobile_number', 'is_active']
    search_fields = ['full_name', 'email', 'mobile_number']
    list_filter = ['is_active']

@admin.register(UserFavouriteSimPlan)
class UserFavouriteSimPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan']
    search_fields = ['user__full_name', 'plan__plan_description']
    list_filter = ['user']
