from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateUser, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
# from complaints.models import Complaint




def generate_jwt(user):
    payload={
        "user_id":user.id,
        "iat":datetime.utcnow(),
       "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return token


@api_view(["Post"])
# @permission_classes([IsAuthenticated])
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

            token=generate_jwt(user)

            # Step 1 - Assign a jwt secret - any random string
            # Step 2 - Create the jwt token where payload is the user.id
            # Step 3 - return the jwt token in the response with property token: "[jwt w=token]"
            return Response(
                {
                    "message":"Login Successful",
                    "token": token
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

