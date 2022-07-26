from django.urls import path
from . import views


app_name = "base"
urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path('create-room/', views.createForm, name="create_room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update_room")
]
