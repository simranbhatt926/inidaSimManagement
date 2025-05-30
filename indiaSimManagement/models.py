from django.db import models
from operatorManagement.models import Operator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class PlanType(BaseModel):
    plan_type = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_type


class PackCategory(BaseModel):
    pack_category = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.pack_category


class PackValidity(BaseModel):
    pack_validity = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.pack_validity


class PackAmount(BaseModel):
    pack_amount = models.FloatField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pack_amount)

    def get_int_price(self):
        return int(self.pack_amount)


class ConnectionType(BaseModel):
    connection_type = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.connection_type



class State(models.Model):
    state =models.CharField(max_length=100,blank=False,null=False)
    is_active = models.BooleanField(default = False)
    state_image = models.ImageField(upload_to='states/')
    iso_code = models.CharField(max_length=5,null=True,blank=True)


    def __str__(self):
        return self.state

class City(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    city =models.CharField(max_length=100,blank=False,null=False)
    is_active = models.BooleanField(default = False)
    is_cod = models.BooleanField(default=False)
    city_image = models.ImageField(upload_to='cities/')


    def __str__(self):
        return self.city
    


class IndiaSimConstants(BaseModel):
    KEY_CHOICES = [
        ('local_delivery_charge', 'local_delivery_charge'),
        ('sim_card_charge', 'sim_card_charge'),
        ('special_delivery_charge', 'special_delivery_charge'),
        ('partial_payment','partial_payment'),
        ('in_demand','in_demand'),
        ('in_stock','in_stock'),
        ('accept_indian_order','accept_indian_order')
    ]
    key = models.CharField(
        max_length=255,
        choices=KEY_CHOICES,
        blank=False,
        null=True  # or False if you want to make it required
    )
    value = models.CharField(max_length=1255000, blank=False, null=True)

    def __str__(self):
        return f"{self.key}: {self.value}"
    

    
class IndiaFRCSimPack(BaseModel):
    CONNECTION_TYPE = (
        ('Prepaid', 'Prepaid'),
        ('Postpaid', 'Postpaid'),
    )

    # choices.py


    operator = models.ForeignKey(Operator, related_name='operator_frc', on_delete=models.CASCADE, null=True)
    connection = models.CharField(max_length=30, default='Prepaid', choices=CONNECTION_TYPE)
    states = models.ManyToManyField(State, blank=True)
    cities = models.ManyToManyField(City, max_length=1000, blank=True)

    plan_description = models.CharField(max_length=5000, blank=False)
    plan_benefits = models.CharField(max_length=5000, blank=False)
    india_sim_url = models.CharField(max_length=200, blank=True)
    validity = models.ForeignKey(PackValidity, related_name='sim_validity_frc', on_delete=models.CASCADE, null=True)
    amount = models.ForeignKey(PackAmount, related_name='sim_amount_frc', on_delete=models.CASCADE, null=True)
    talktime = models.CharField(max_length=100, blank=True, null=True)
    sms = models.CharField(max_length=100, blank=True, null=True)
    data = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    priority = models.IntegerField( blank=True, null=True,default=10)
    is_active = models.BooleanField(default=True)
    favourite_marked = models.BooleanField(default=True)
    extra_charge = models.CharField(max_length=100, blank=True, null=True, default="0")
    selected_favourite = models.BooleanField(default=False)
    offer_price = models.CharField(max_length=100, blank=True, null=True)
    traveller_plan = models.BooleanField(default=False)
    best_data_uasage = models.BooleanField(default=False)
    most_affordable = models.BooleanField(default=False)

    constants = models.ManyToManyField(IndiaSimConstants, blank=True)




    def __str__(self):
        return self.plan_description
    
# class ImageUpload(models.Model):
#     img = models.ImageField(upload_to='uploads/images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     hero_section = models.BooleanField(default=False)
#     image_name = models.CharField(max_length=100,null=True,blank=True)
#     page_name = models.CharField(max_length=100,null=True,blank=True)


class AcceptedPinCode(models.Model):
    pin_code = models.CharField(max_length=20, blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) # add this line
    is_cod = models.BooleanField(default=False)

    def __str__(self):
        return self.pin_code


