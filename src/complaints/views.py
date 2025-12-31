from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response    
from rest_framework import status
from .serializers import CreateComplaints, UpdateComplaintStatus
from .models import Complaint
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def verify_jwt(token):
    print("token in token", token)
    if not token:
        raise AuthenticationFailed("Token Missing")

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        user_id=payload.get("user_id")
        print("purva kkk", user_id)

        if not user_id:
            raise AuthenticationFailed("Invalid token payload")
        return user_id
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token expired")
    
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Token Missing")




def get_token(request):
    auth_header=request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        prefix, token= auth_header.split(" ")
        if prefix != 'Bearer':
            return None

        return token
    except ValueError:
        return None


# STATIC_USERNAME="purva29"
@api_view(['Post'])
def create_complaint(request):
    serializer = CreateComplaints(data=request.data)
    # username="purva29"
    print("request", request.headers)
    jwt_token = get_token(request)
    print("jwt token", jwt_token)
    user_id = verify_jwt(jwt_token)
    print("p1", user_id)

    
    if serializer.is_valid():

        #get the user first from the user id
        user = User.objects.get(id=user_id)
        print("pbk", user)

        complaint= Complaint.objects.create(
            user=user,
            title=request.data.get('title'),
            description=request.data.get('description'),
            priority=request.data.get('priority'),
        )

        return Response(
            {
                "complaint_id": complaint.id,
                "message":"Complaint created",
                "user": user.id
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_complaint(request):
    # complaints=Complaint.objects.all()
    complaints=Complaint.objects.filter(user=request.user)

    data=[]
    for c in complaints:
        data.append(
            {
                "id":c.id,
                "title": c.title,
                "description": c.description,
                "status":c.status,
                "priority":c.priority,
                "time":c.created_at
            }
        )

    return Response(data)



@api_view(['GET'])
def get_single_complaint(request, complaint_id):
    # complaints= Complaint.objects.filter(user_username=username)
    try:

        # First verify the jwt token
        jwt_token = get_token(request)
        user_id = verify_jwt(jwt_token)
        # is get the complaint
        complaint_info = Complaint.objects.get(id=complaint_id)
        # is check the complaint user id with the user id in the token
        if complaint_info.user_id != user_id:
            raise AuthenticationFailed("you are not eligible to access this data currently.")
        # then return complaint information
        return Response({
            "id": complaint_info.id,
            "title":complaint_info.title,
            "description":complaint_info.description,
            "status":complaint_info.status,
            "priority":complaint_info.priority,
            "time":complaint_info.created_at
        })  

    except Complaint.DoesNotExist:
        return Response(
            {
                "error": "Can't find complaint"
            },
            status=status.HTTP_404_NOT-FOUND
        )

@api_view(['PATCH'])
def update_complaint_status(request):
    # complaints= Complaint.objects.filter(user_username=username)
    

    try:
        serializer = UpdateComplaintStatus(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        jwt_token = get_token(request)
        user_id = verify_jwt(jwt_token)
        complaint_id = request.data.get("id")
        complaint_info = Complaint.objects.get(id=complaint_id)
        if complaint_info.user_id != user_id:
            raise AuthenticationFailed("you are not eligible to access this data currently.")

        complaint_info.status = request.data.get("status")
        complaint_info.save()
        return Response({
            "id": complaint_info.id,
            "title":complaint_info.title,
            "description":complaint_info.description,
            "status":complaint_info.status,
            "priority":complaint_info.priority,
            "time":complaint_info.created_at
        })  

    except Complaint.DoesNotExist:
        return Response(
            {
                "error": "Can't find complaint"
            },
            status=status.HTTP_404_NOT-FOUND
        )




# Tomorrow Morning
# Create Complaint api -DONE
# list complaint api - Done
# get complaint based on the user name- done
# Update complaint status api - done
# Django signals to update the status automatically - done
# Machine Learning - Complaints data sets to update the priority
# Langgraph and langchain