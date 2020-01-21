from django.urls import path
from app_personal import views

urlpatterns = [
    path('', views.login)
]

