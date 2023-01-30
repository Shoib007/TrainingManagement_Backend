from rest_framework import serializers
from .models import TrainerDetails
class TrainerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerDetails
        fields = '__all__'
        