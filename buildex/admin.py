from django.contrib import admin
from .models import *
# from .models import CheckoutPreviewAPIView
# admin.site.register(CheckoutPreviewAPIView)

# comment


# @admin.register(Checkout)
# class CheckoutAdmin(admin.ModelAdmin):
#     list_display = ('user', 'plan', 'operator', 'connection_mode', 'payment_method')
#     search_fields = ('user__full_name', 'user__email', 'plan__plan_name', 'payment_method')
#     list_filter = ('payment_method', 'operator', 'connection_mode')

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('checkout', 'payment_type', 'paid_now', 'pay_later_mode', 'transaction_id', 'created_at')
#     search_fields = ('checkout__user__full_name', 'transaction_id', 'payment_type')
#     list_filter = ('payment_type', 'pay_later_mode', 'created_at')
