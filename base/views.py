from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from .models import Room, Message, Topic
from .forms import RoomForm
# Create your views here.

def home(request):
    
    q = request.GET.get('q')
    #if q is not None or not '' then filter the rooms if they have messages that contain the topic q
    rooms = Room.objects.filter(Q(message__topic__name__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)) if request.GET.get('q') != None and request.GET.get('q') != '' else Room.objects.all()
    room_count = rooms.count()
    
    #rooms = Room.objects.all() #all() returns a QuerySet with all the rooms in the database
    topics = Topic.objects.all()
    #get the number of messages in each room

    room_messages = (Message.objects.values('room').annotate(dcount = Count('room')).order_by())

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):

    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room)
    context = {'room': room, 'messages': messages}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)
    
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)

