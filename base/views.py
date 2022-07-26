
from django.shortcuts import redirect, render

from .form import RoomForm
from .models import Room

# Create your views here.

rooms_ = [
    {'id': 1, 'name': "Let's learn python"},
    {'id': 2, 'name': "Let's design together"},
    {'id': 3, 'name':"Frontend Developers"}
]

def home(request):
    rooms = Room.objects.all() 
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, pk):

    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, 'base/room.html', context)


def createForm(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('base:home')

    context = {"form": form}
    return render(request, 'base/room_form.html', context)



def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance= room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:home')

    context = {"form": form}
    return render(request, 'base/room_form.html', context)
