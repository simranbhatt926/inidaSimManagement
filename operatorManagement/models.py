from django.db import models
from countryManagement.models import Country

# Create your models here.
class Operator(models.Model):
 OPERATOR_TYPE = (
 ('PREPAID', 'PREPAID'),
 ('MOBILE', 'MOBILE'),
 ('DTH', 'DTH'),
 ('POSTPAID', 'POSTPAID'),
 ('ELECTRICITY', 'ELECTRICITY'),
 ('WATER', 'WATER'),
 ('OTHER', 'OTHER'),
 )
 country = models.ForeignKey(Country, related_name='operator_country', on_delete=models.CASCADE, null=True)
 operator_image = models.ImageField(upload_to='operator/', null=True)
 operator_name = models.CharField(max_length=100, blank=True, null=True)
 operator_code = models.CharField(max_length=20, blank=True, null=True)
 operator_type = models.CharField(max_length=20, choices=OPERATOR_TYPE, default='MOBILE')
 operator_category = models.CharField(max_length=50, default='', blank=True)
 operator_source = models.CharField(max_length=20, default='JOLO')
 additional_parameters = models.JSONField(null=True)
 is_active = models.BooleanField(default=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateField(auto_now=True)
 
 def __str__(self):
   return str(self.operator_code)


class Circle(models.Model):
 country = models.ForeignKey(Country, related_name='circle_country', on_delete=models.CASCADE, null=True)
 circle = models.CharField(max_length=50, blank=True, null=True)
 bbps_coverage = models.CharField(max_length=50, blank=True, null=True)
 coverage_area = models.CharField(max_length=500, blank=True, null=True, default='')
 circle_code = models.CharField(max_length=10, blank=True, null=True)
 slug = models.SlugField(unique=True, blank=True, null=True, max_length=10000)
 is_active_to_buy = models.BooleanField(default=False)
 is_active = models.BooleanField(default=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateField(auto_now=True)

 def __str__(self):
    return str(self.circle)
 