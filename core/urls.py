from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stat/', views.stat, name='stat'),
    path('download/', views.download, name='download'),
    path('logout/', views.do_logout, name='logout'),
]
