from rest_framework import serializers
from .models import TrainerDetails, TrainingDetails, schoolDetail, Users
class TrainerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerDetails
        fields = '__all__'


class TrainingSerializer(serializers.ModelSerializer):
    trainerName = serializers.PrimaryKeyRelatedField(queryset=TrainerDetails.objects.all())
    schoolName = serializers.PrimaryKeyRelatedField(queryset=schoolDetail.objects.all())
    class Meta:
        model = TrainingDetails
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['trainerName'] = instance.trainerName.fname  # replace `name` with the field you want to return
        rep['TrainerLink'] = instance.trainerName.trainerLink
        rep['schoolName'] = instance.schoolName.school  # replace `name` with the field you want to return
        return rep
        
class schoolDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = schoolDetail
        fields = '__all__'

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name','email','password','phoneNumber','is_staff']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance
