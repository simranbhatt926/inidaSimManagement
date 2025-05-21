from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Country(models.Model):
    country_code = models.CharField(max_length=4, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    country_iso2 = models.CharField(max_length=5, blank=True, null=True)
    slug = models.CharField(max_length=200, blank=True, null=True)
    country_image = models.CharField(max_length=200, blank=True, null=True)
    country_image_2 = models.ImageField(upload_to='country', null=True, blank=True, default="")
    iso3 = models.CharField(max_length=200, blank=True, null=True)
    priority = models.IntegerField(blank= True, null=True )
    is_top = models.BooleanField(default=False)
    is_home = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateField(auto_now=True,null=True,blank=True) 
    
    def __str__(self):
       return self.country_name 
    
    def get_absoulte_url(self,pre_url = 'buy-international-esim' , type = '-esim'):
        if self.slug:
            return '/'+pre_url+'/'+self.slug+type+'/'
 

 
class BannerImageModel(BaseModel):
    Bannertitle = models.CharField(max_length=100)
    Bannerimage = models.ImageField(upload_to='banners/')