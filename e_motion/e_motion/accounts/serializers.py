from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['pk','first_name', 'last_name',]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'date_of_birth',
            'subscription_plan',
            'subscription_start_date',
            'subscription_end_date',
            'attendance_count',
            'attended_trainings',
            'user'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        return super().update(instance, validated_data)