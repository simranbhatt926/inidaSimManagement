# # from django.db import models
# # # from django.contrib.auth.models import User
# # from user.models import *
# # # from indiaSimManagement.models import IndiaFRCSimPack, Operator, ConnectionMode  # Use correct app and models
# # from indiaSimManagement.models import IndiaFRCSimPack, ConnectionType
# # from operatorManagement.models import Operator


# # PAYMENT_CHOICES = [
# #     ('FULL', 'Full Payment'),
# #     ('COD', 'Cash On Delivery'),
# #     ('PARTIAL', 'Partial Payment'),
# # ]

# # class Checkout(models.Model):
# #     # user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
# #     plan = models.ForeignKey(IndiaFRCSimPack, on_delete=models.CASCADE)  # using correct plan model
# #     operator = models.ForeignKey(Operator, on_delete=models.CASCADE, default=1)

# #     connection_mode = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, default=1)

# #     payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES,default=1)

# # class Payment(models.Model):
# #     checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
# #     payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
# #     paid_now = models.DecimalField(max_digits=10, decimal_places=2, default=0)
# #     pay_later_mode = models.CharField(max_length=10, choices=[('COD', 'COD'), ('ONLINE', 'Online')], null=True, blank=True)
# #     transaction_id = models.CharField(max_length=255, null=True, blank=True)
# #     created_at = models.DateTimeField(auto_now_add=True)



# # update code 
# from django.db import models
# from user.models import *
# from indiaSimManagement.models import IndiaFRCSimPack, ConnectionType
# from operatorManagement.models import Operator

# # Payment options
# PAYMENT_CHOICES = [
#     ('FULL', 'Full Payment'),
#     ('COD', 'Cash On Delivery'),
#     ('PARTIAL', 'Partial Payment'),
# ]

# class Checkout(models.Model):
#     user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
#     plan = models.ForeignKey(IndiaFRCSimPack, on_delete=models.CASCADE)
#     operator = models.ForeignKey(Operator, on_delete=models.CASCADE, default=1)
#     connection_mode = models.ForeignKey(ConnectionType, on_delete=models.CASCADE, default=1)
    
#     # 👇 Here you update payment_method with verbose_name and correct default
#     payment_method = models.CharField(
#         max_length=50,
#         choices=PAYMENT_CHOICES,
#         default='FULL',
#         verbose_name="Payment Method"
#     )

#     def __str__(self):
#         return f"{self.user} - {self.plan} - {self.payment_method}"


# class Payment(models.Model):
#     checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
#     payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
#     paid_now = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     pay_later_mode = models.CharField(max_length=10, choices=[('COD', 'COD'), ('ONLINE', 'Online')], null=True, blank=True)
#     transaction_id = models.CharField(max_length=255, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.payment_type} - ₹{self.paid_now}"

from django.db import models
# from django.contrib.auth.models import User
from user.models import *

class Operator(models.Model):
    name = models.CharField(max_length=100)

class Plan(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class UserFavouritePlan(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    connection_mode = models.CharField(max_length=50)
