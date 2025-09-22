from django.urls import path, include
from . import views

app_name  = 'webapp'
urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.index, name='test'),
    path('pairplot/', views.show_pairplot, name='pairplot'),
    path('heatmap/', views.show_heatmap, name='heatmap'),
    path('pjt_desc/', views.project, name='project'),
    path('predict/', views.predict_view, name='predict'),
]
