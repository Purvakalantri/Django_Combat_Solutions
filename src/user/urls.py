from django.urls import path
from .views import create_user
from .views import user_login

urlpatterns = [
    path("create_user", create_user),
    path("user_login", user_login)
]