from django.urls import path
from . import views

urlpatterns = [
    path('endpoint/', views.api_endpoint, name='api_endpoint'),
    path('download/', views.download_data, name='download_data'),
]