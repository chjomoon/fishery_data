from django.urls import path, include
from . import views

app_name  = 'firstapp'
urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.index, name='test'),
]
