from .models import *
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'



class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerImageModel
        fields = ['id', 'Bannertitle', 'Bannerimage', 'created_at']