from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'ToP/home.html')

def top_rated(request):
    # create context_dict here to pass playlists sorted by rates into template
    return render(request, 'ToP/top_rated.html')

def most_listened(request):
    return render(request, 'ToP/most_listened.html')

def show_playlist(request):
    return render(request, 'ToP/playlist.html')

def login(request):
    return render(request, 'ToP/login.html')

def register(request):
	return render(request, 'ToP/register.html')
	