from django.shortcuts import render
from django.http import HttpResponse
from ToP.forms import PlaylistForm, SongForm

def home(request):
    return render(request, 'ToP/home.html')

def top_rated(request):
    # create context_dict here to pass playlists sorted by rates into template
    return render(request, 'ToP/top_rated.html')

def most_listened(request):
    return render(request, 'ToP/most_listened.html')

def show_playlist(request):
    return render(request, 'ToP/playlist.html')

def view_all_playlists(request):
    return render(request, 'ToP/view_all_playlists.html')

"""@login_required"""
def my_playlists(request):
    return render(request, 'ToP/my_playlist.html')

"""@login_required"""
def create_playlists(request):
    form = PlaylistForm()

    if request.method == 'POST':
        form=PlaylistForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return home(request)
        else:
            print(form.errors)
            
    return render(request,'ToP/create_playlist.html', {'form': form})

"""@login_required"""
def add_Song(request):
    form = SongForm()

    if request.method == 'POST':
        form=SongForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return create_playlist(request)
        else:
            print(form.errors)

    return render(request,'ToP/add_song.html', {'form': form})
