from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.lobby,name='lobby'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',success_url='/'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('create-room/<str:username>/', views.create_room, name='create_room'),
]