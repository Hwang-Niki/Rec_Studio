from django.urls import path
from . import views  
from .views import  create_project, delete_project
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('studio/artist_form/', views.artist, name='artist'), 
    path('studio/producer_form/', views.producer, name='producer'),
    path('studio/client/', views.client, name='client'),
    path('studio/notifications/', views.notification, name='notifications'),
    path('studio/notifications_client/', views.notification_client, name='notifications_client'),
    path('studio/project/', views.project, name='projects'),
    path('studio/project/create/', create_project, name='create_project'),
    path('studio/project/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
