from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateUser, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
    

@api_view(["Post"])
def create_user(request):
    serializer = CreateUser(data=request.data)

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
            status=status.HTTP_201_CREATED

        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["Post"])
def user_login(request):
    
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password) 
        print("bharat", user)

        if user is not None:
            return Response(
                {
                    "message":"Login Successful"
                },
                status = status.HTTP_200_OK
            ) 

        else:
            return Response(
                {
                    "error":"Invalid username or password"
                },
                status= status.HTTP_401_UNAUTHORIZED
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

