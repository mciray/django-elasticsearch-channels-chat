from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.http import JsonResponse

from chat.documents import ArticleDocument
def search_articles(request):
    
    q = request.GET.get('q', '')
    if q:
        articles = ArticleDocument.search().query("match", title=q).to_queryset()
        results = [{'title': article.title, 'id': article.id} for article in articles]
    else:
        results = []
    return JsonResponse({'results': results})
@login_required
def lobby(request):
    users = User.objects.exclude(username=request.user.username)
    q = request.GET.get('q', '')  
    articles = ArticleDocument.search().query("match", title=q).to_queryset() if q else []
    return render(request, 'chat/lobby.html', {'users': users, 'articles': articles})

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
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
    room_name = f"{request.user.username}_{username}"  
    return HttpResponseRedirect(reverse('room', args=[room_name]))

def logout_view(request):
    logout(request)
    return redirect('lobby') 