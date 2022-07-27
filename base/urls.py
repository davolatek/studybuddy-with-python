from django.urls import path
from . import views


app_name = "base"
urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path('create-room/', views.createForm, name="create_room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update_room"),
    
]
