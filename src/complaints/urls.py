from django.urls import path
from .views import create_complaint
from .views import get_complaint
from .views import get_single_complaint, update_complaint_status


urlpatterns=[
    path('create_complaint', create_complaint),
    path('get_complaint', get_complaint),
    path('update_complaint_status', update_complaint_status),
    path('get_complaint_by_id/<int:complaint_id>', get_single_complaint)
    
]