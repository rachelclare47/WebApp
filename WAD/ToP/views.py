from django.shortcuts import render
from django.http import HttpResponse
from ToP.forms import PlaylistForm, SongForm
from ToP.models import Playlist, Song

def home(request):
    return render(request, 'ToP/home.html')

def top_rated(request):
    # create context_dict here to pass playlists sorted by rates into template
    return render(request, 'ToP/top_rated.html')

def most_listened(request):
    return render(request, 'ToP/most_listened.html')

def show_playlist(request, playlist_name_slug):
    context_dict = {}
    try:
        # Can we find a playlist with the given name slug? 
        # If not, .get() method raises a DoesNotExist exception
        # If yes, .get() returns one model instance
        playlist = Playlist.objects.get(slug=playlist_name_slug)
        # Retrieve all associated songs
        # filter() returns a list of song objects or an empty list
        songs = Song.objects.filter(playlists=playlist)
        # Add filtered list to dict
        context_dict['songs'] = songs
        context_dict['playlist'] = playlist
    except Playlist.DoesNotExist:
        # Template will display "no playlist" message for us
        context_dict['playlist'] = None
        context_dict['songs'] = None
        
    return render(request, 'ToP/playlist.html', context_dict)


def view_all_playlists(request):
    # Get a list of all playlists currently stored and order by name ascending
    playlist_list = Playlist.objects.order_by('name')
    # List placed into context dictionary that is passed into template engine
    context_dict = {'playlists': playlist_list}
    
    return render(request, 'ToP/view_all_playlists.html', context_dict)

"""@login_required"""
def my_playlists(request):
    return render(request, 'ToP/my_playlist.html')

"""@login_required"""
def create_playlists(request):
    """form = PlaylistForm()

    if request.method == 'POST':
        form=PlaylistForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return home(request)
        else:
            print(form.errors)"""
            
    return render(request, 'ToP/create_playlist.html')

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

def login(request):
    return render(request, 'ToP/login.html')

def register(request):
	return render(request, 'ToP/register.html')
	
