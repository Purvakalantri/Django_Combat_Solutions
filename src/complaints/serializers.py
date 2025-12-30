from rest_framework import serializers
# from django.contrib.auth.models import User


@api_view(['Post'])
class createcomplaint(serializers.Serializer):
    title= serializers.CharField(max_length=100)
    description=serializers.CharField(min_length=100, max_length=400)
    

    