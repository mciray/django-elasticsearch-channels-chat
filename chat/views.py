from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Message
from chat.documents import MessageDocument
def search_articles(request):
    q = request.GET.get('q', '')
    if q:
        messages = MessageDocument.search().query("match", content=q).to_queryset()
        results = [{'username': message.user.username, 'id': message.id, 'content': message.content} for message in messages]
    else:
        results = []
    return JsonResponse({'results': results})

@login_required
def lobby(request):
    users = User.objects.exclude(username=request.user.username)
    
    return render(request, 'chat/lobby.html', {'users': users})

@login_required
def room(request, room_name):
    messages = Message.objects.filter(room=room_name).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_room(request, username):
    
    sorted_usernames = sorted([request.user.username, username])
    room_name = "_".join(sorted_usernames)

    # Oluşturulan oda adıyla 'room' view'ına yönlendir
    return redirect(reverse('room', args=[room_name]))
def logout_view(request):
    logout(request)
    return redirect('lobby') 