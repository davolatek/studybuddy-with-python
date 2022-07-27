
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .form import RoomForm
from .models import Room, Topic

# Create your views here.

# rooms_ = [
#     {'id': 1, 'name': "Let's learn python"},
#     {'id': 2, 'name': "Let's design together"},
#     {'id': 3, 'name':"Frontend Developers"}
# ]


def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, "Incorrect username or password")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('base:home')
    

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, "An error occured during registration")
    context = {'page': page, 'form': form}


    return render(request, 'base/login_register.html', context)

def home(request):

    if not request.user.is_authenticated:
        return redirect('base:login')

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains = q)
        ) 
    room_count = rooms.count()
    topic = Topic.objects.all()
    context = {'rooms': rooms, 'topics':topic, 'room_count':room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):

    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, 'base/room.html', context)


@login_required(login_url= 'base:login')
def createForm(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('base:home')

    context = {"form": form}
    return render(request, 'base/room_form.html', context)



@login_required(login_url= 'base:login')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance= room)


    if request.user != room.host:
        return HttpResponse("You can not update a room profile you did not create")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:home')

    context = {"form": form}
    return render(request, 'base/room_form.html', context)
