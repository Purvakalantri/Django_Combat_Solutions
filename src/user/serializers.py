from rest_framework import serializers
from django.contrib.auth.models import User



class CreateUser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    first_name = serializers.CharField(max_length=10)
    last_name = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        print("python reaches login serializer")

    def validate_email(self, value):
        print("purva came here")
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError("Email is invalid , provide valid email")
        return value


class LoginSerializer(serializers.Serializer):
    print("python reaches login serializer")
    username=serializers.CharField(max_length=10)
    password=serializers.CharField(write_only=True)

        
    