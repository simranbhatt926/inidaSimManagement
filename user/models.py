from django.db import models

# from indiaSimManagement.models import IndiaFRCSimPack
from indiaSimManagement.models import *

# class UserInfo(models.Model):
#     full_name = models.CharField(max_length=100)
#     mobile_number = models.CharField(max_length=15)
#     address = models.TextField()
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.full_name

# update userinofo using password
class UserInfo(models.Model):
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128,default='default123')  # Store hashed password
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class UserFavouriteSimPlan(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    plan = models.ForeignKey(IndiaFRCSimPack, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.full_name} - {self.plan.plan_description}"