from django.urls import path
from app import views

urlpatterns = [
    path('', views.health_check, name='health check')
]
