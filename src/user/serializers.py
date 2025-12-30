from rest_framework import serializers
from django.contrib.auth.models import User



class CreateUser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # print("saurabh", serializers.CharField)
    first_name = serializers.CharField(max_length=10)
    last_name = serializers.CharField(max_length=10)  #for having max_length
    # email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        print("purva came here")
        if not value.endswith("@gmail.com"):
            raise serializers.ValidationError("Email is invalid , provide valid email")
        return value


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=10)
    password=serializers.CharField(write_only=True)

        
    