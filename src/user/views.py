from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User

@api_view(["Post"])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = User.objects.create_user(
            
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name'),
            email=serializer.validated_data['email'],
            password= serializer.validated_data['password']
        )

        print("heloo there,", user)

        return Response(
            {
                "message": "User created successfully",
                "user" : serializer.validated_data                
            },
            status= status.HTTP_200_CREATED 

        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

