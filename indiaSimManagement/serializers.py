
from .models import IndiaSimConstants
# from userManagement.models import Cart
from .models import *
from operatorManagement.serializers import *
from rest_framework import serializers



class FRCSimPackNewSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer(read_only=True)
    circle = serializers.StringRelatedField()
  
    validity = serializers.StringRelatedField()
    amount = serializers.StringRelatedField()

    class Meta:
        model = IndiaFRCSimPack
        exclude = ('created_at', 'is_active', )



class IndiaFRCSimPackSerializer(serializers.ModelSerializer):
    operator = serializers.SerializerMethodField()
    constants = serializers.SerializerMethodField()

    class Meta:
        model = IndiaFRCSimPack
        fields = '__all__'

    def get_operator(self, obj):
        request = self.context.get('request')
        image_url = ''
        if obj.operator and obj.operator.operator_image:
            if str(obj.operator.operator_image).startswith('http'):
                image_url = obj.operator.operator_image
            elif request:
                image_url = request.build_absolute_uri(obj.operator.operator_image.url)
            else:
                image_url = obj.operator.operator_image.url

        return {
            "operator_name": obj.operator.operator_name if obj.operator else "",
            "operator_code": obj.operator.operator_code if obj.operator else "",
            "operator_image": image_url
        }
    

    def get_constants(self, obj):
        constants = IndiaSimConstants.objects.all()
        return {const.key: const.value for const in constants}


class StateSerializer(serializers.ModelSerializer):
    state_image = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ['id', 'state', 'is_active', 'state_image']
        read_only_fields = ['id']


    class Meta:
        model = State
        fields = ['id', 'state', 'is_active', 'state_image']
        read_only_fields = ['id']

    def get_state_image(self, obj):
        request = self.context.get('request')
        if obj.state_image and hasattr(obj.state_image, 'url'):
            scheme = 'https' if request and request.is_secure() else 'http'
            domain = request.get_host() if request else 'localhost'
            return f"{scheme}://{domain}{obj.state_image.url}"
        return None


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)
    city_image = serializers.SerializerMethodField()

    state_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(),
        source='state',
        write_only=True
    )

    class Meta:
        model = City
        fields = ['id', 'state', 'state_id', 'city', 'is_active', 'is_cod', 'city_image']
        read_only_fields = ['id']

    def get_city_image(self, obj):
        request = self.context.get('request')
        if obj.city_image and hasattr(obj.city_image, 'url'):
            scheme = 'https' if request and request.is_secure() else 'http'
            domain = request.get_host() if request else 'localhost'
            return f"{scheme}://{domain}{obj.city_image.url}"
        return None

    

# class ImageUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageUpload
#         fields = ['id', 'image', 'uploaded_at']




# Comment cart line

# class CartSerializer(serializers.ModelSerializer):
#     sim_pack = IndiaFRCSimPackSerializer(read_only=True)
#     sim_pack_id = serializers.PrimaryKeyRelatedField(
#         queryset=IndiaFRCSimPack.objects.all(), source='sim_pack', write_only=True
#     )

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'sim_pack', 'sim_pack_id', 'is_ordered']
#         read_only_fields = ['user', 'is_ordered']


class IndiaSimConstantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndiaSimConstants
        fields = ['id', 'key', 'value']