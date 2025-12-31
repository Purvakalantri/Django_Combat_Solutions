from rest_framework import serializers
from .models import Complaint

class CreateComplaints(serializers.ModelSerializer):

    title= serializers.CharField(max_length=100)
    description=serializers.CharField(min_length=100, max_length=400)
    # complaint_id=serializers.IntegerField(source='id', read_only=True)
    


    class Meta:
        model=Complaint
        fields=[ 'title', 'description']


class UpdateComplaintStatus(serializers.ModelSerializer):
    class Meta:
        model=Complaint
        fields=[ 'id', 'status']
    