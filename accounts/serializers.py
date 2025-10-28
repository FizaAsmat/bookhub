from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSignupSerializer(serializers.ModelSerializer):
    # Extra fields
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.Role_Choices)  # from your Profile model

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Create related Profile with role
        Profile.objects.create(user=user, role=role)
        return user
