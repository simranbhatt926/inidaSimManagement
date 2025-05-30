# from .models import UserInfo, UserFavouriteSimPlan
# from indiaSimManagement.models import IndiaFRCSimPack
# from rest_framework import serializers

# class FavouritePlanDetailSerializer(serializers.ModelSerializer):
#     plan_description = serializers.CharField(source='plan.plan_description')
#     connection = serializers.CharField(source='plan.connection')
#     operator_name = serializers.CharField(source='plan.operator.operator_name')

#     class Meta:
#         model = UserFavouriteSimPlan
#         fields = ['plan_description', 'connection', 'operator_name']


# class UserFavouritePlanSerializer(serializers.ModelSerializer):
#     favourite_plans = serializers.SerializerMethodField()

#     class Meta:
#         model = UserInfo
#         fields = ['id', 'full_name', 'email', 'favourite_plans']

#     def get_favourite_plans(self, obj):
#         plans = UserFavouriteSimPlan.objects.filter(user=obj)
#         return FavouritePlanDetailSerializer(plans, many=True).data


# class UserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInfo
#         fields = '__all__'



from rest_framework import serializers
from .models import *
from indiaSimManagement.models import IndiaFRCSimPack, IndiaSimConstants
from operatorManagement.models import Operator
from datetime import datetime
from indiaSimManagement.models import State, City, PackValidity, PackAmount
from django.contrib.auth.hashers import make_password, check_password


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ['operator_name', 'operator_code', 'operator_image']


class PlanConstantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndiaSimConstants
        fields = ['key', 'value']


# class FullPlanSerializer(serializers.ModelSerializer):
class FullPlanSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer()
    constants = serializers.SerializerMethodField()
    states = serializers.SlugRelatedField(slug_field='state', many=True, read_only=True)
    cities = serializers.SlugRelatedField(slug_field='city', many=True, read_only=True)
    validity = serializers.SlugRelatedField(slug_field='pack_validity', read_only=True)
    amount = serializers.SlugRelatedField(slug_field='pack_amount', read_only=True)
    current_time = serializers.SerializerMethodField()

    class Meta:
        model = IndiaFRCSimPack
        fields = '__all__'  # to include all fields including ones below

    def get_constants(self, obj):
        constants = obj.constants.all()
        return {item.key: item.value for item in constants}

    def get_current_time(self, obj):
        now = datetime.now()
        return now.strftime('%d-%m-%Y %H:%M:%S')

class UserFavouritePlanSerializer(serializers.ModelSerializer):
    favourite_plans = serializers.SerializerMethodField()

    class Meta:
        model = UserInfo
        fields = ['id', 'full_name', 'email', 'favourite_plans']

    def get_favourite_plans(self, obj):
        favourite_links = UserFavouriteSimPlan.objects.filter(user=obj)
        plans = [link.plan for link in favourite_links]
        return FullPlanSerializer(plans, many=True, context=self.context).data
        # 
        # update user info 
# class UserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserInfo
#         fields = '__all__'
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['full_name', 'mobile_number', 'address', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email_or_mobile = serializers.CharField()
    password = serializers.CharField()
# add user favourite sim plan
class FavouritePlanCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = UserFavouriteSimPlan
        fields = ['user', 'plan', 'created_at']

    def get_created_at(self, obj):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
