from django.shortcuts import render
from django.http import HttpResponse
from ToP.forms import PlaylistForm, SongForm, UserForm, UserProfileForm
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