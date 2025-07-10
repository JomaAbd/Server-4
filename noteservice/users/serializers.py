from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User 
        fields = ('email', 'password')

    def create(self, validated_date):
        return User.objects.create_user(**validated_date)
    
    