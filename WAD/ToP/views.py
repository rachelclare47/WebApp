from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ToP.forms import PlaylistForm, SongForm, UserForm, UserProfileForm
from ToP.models import Playlist, Song
from django.contrib.auth import logout, authenticate
from django.core.urlresolvers import reverse
from datetime import datetime
import spotipy
import sys
import urllib
import os
import shutil
spotify = spotipy.Spotify()


def home(request):
    return render(request, 'ToP/home.html')

def top_rated(request):
    # create context_dict here to pass playlists sorted by rates into template
    return render(request, 'ToP/top_rated.html')

def most_listened(request):
    return render(request, 'ToP/most_listened.html')

def most_listened(request):
    return render(request, 'ToP/most_listened.html')

def most_viewed(request):
    return render(request, 'ToP/most_viewed.html')


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

        #Flushes the artist art folder to prevent build up of unecessary art
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists(BASE_DIR+'\media\\'+"artist_art\\"):
            shutil.rmtree(BASE_DIR+'\media\\'+"artist_art\\")
            os.makedirs(BASE_DIR+'\media\\'+"artist_art\\")
        elif not os.path.exists(BASE_DIR+'\media\\'+"artist_art\\"):
            os.makedirs(BASE_DIR+'\media\\'+"artist_art\\")

        #Queries the spotify song database and pulls the artist image url from it based on the artist title entered on
        #each song. This is called song.album_art
        for song in songs:
            results = spotify.search(q='artist:' + song.artist, type='artist')
            items = results['artists']['items']
            if len(items) > 0:
                artist = items[0]
            song.album_art =artist['images'][0]['url']

            testfile = urllib.URLopener()
            testfile.retrieve(song.album_art,BASE_DIR+'\media\\'+"artist_art\\"+str(song.artist)+"_art.jpg")
            song.art='\media\\'+"artist_art\\"+str(song.artist)+"_art.jpg"
        context_dict['album_art']=song.art
            
    except Playlist.DoesNotExist:
        # Template will display "no playlist" message for us
        context_dict['playlist'] = None
        context_dict['songs'] = None


    visitor_cookie_handler(request)
    context_dict['visits']=request.session['visits']

    #sends the response to the template
    response = render(request, 'ToP/playlist.html',context=context_dict)
 
    return response


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
def create_playlist(request):
    form = PlaylistForm()

    if request.method == 'POST':
        form = PlaylistForm(request.POST)

        # Valid form?
        if form.is_valid():
            form.save(commit=True)
            return home(request)
        else:
            print(form.errors)
            
    # Render form with error messages, if any
    return render(request, 'ToP/create_playlist.html', {'form': form})


"""@login_required"""
def add_song(request, playlist_name_slug):
    try:
        playlist = Playlist.objects.get(slug=playlist_name_slug)
    except Playlist.DoesNotExist:
        playlist = None
        
    form = SongForm()
    
    if request.method == 'POST':
        form = SongForm(request.POST)

        if form.is_valid():
            if playlist:
                song = form.save(commit=False)
                song.playlists = playlist
                song.save()
                return show_playlist(request, playlist_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'playlist': playlist}
    return render(request, 'ToP/add_song.html', context_dict)


def register(request):
    # A boolean value for telling the template whether
    # the registration was successful.
    # Set to False initially. I the registration is
    # successful it is changed to True.
    registered = False

    # If it's a HTTP Post method then we are interested in processing the
    # form data
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both the user form and the user
        # profiile form.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the users form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfle instance
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so we need to get it from the user profile form and
            # put it in the UserProfile model.
            if 'picture' in request.files:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful
            registered = True
        else:
            # invalid form or forms - mistakes or something else?
            # print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render the template depending on the context
    return render(request, 'registration/registration_form.html',
        {'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information
    if request.method() == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct
        # If we have None, no user with those credentials was found
        if user:
            # Is the account active? It could have been disabled
            if user.is_active:
                # If the user is active and valid, we can log the user in.
                # We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used, no logging in!
                return HttpResponse("This account has been disabled.")
        else:
            # Bad login details were provided, so we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details provided.")

    # The request is not a HTTP POST, so we display the login form
    # This scenario would most likely be a HTTP GET
    else:
        return render, 'registration/auth_login.html', {}


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def get_server_side_cookie(request,cookie,default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    #Gets the number of views of the site
    #If the cookie exists, the string value is cast to an integer value and returned
    #Otherwise 1 is used as the default value
    visits = int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days>0:
        visits=visits+1
        request.session['last_visit']=str(datetime.now())
    else:
        visits = 1
        request.session['last_visit']= last_visit_cookie

    request.session['visits']=visits
    
