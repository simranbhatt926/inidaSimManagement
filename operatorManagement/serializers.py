from rest_framework import serializers
from .models import Operator, Circle
class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ( 'operator_name', 'operator_code', 'operator_image')


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ('circle', 'coverage_area','circle_code','slug','is_active','is_active_to_buy')



class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'