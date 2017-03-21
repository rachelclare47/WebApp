from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ToP.forms import PlaylistForm, SongForm, UserForm, UserProfileForm, CommentForm
from ToP.models import Playlist, Song, UserProfile
from django.contrib.auth import logout, authenticate
from django.core.urlresolvers import reverse
from datetime import datetime
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import resolve_url, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
                                 logout as auth_logout, get_user_model, update_session_auth_hash)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django import forms
from django.core.mail import send_mail

import spotipy
import sys
import urllib
import os
import shutil

spotify = spotipy.Spotify()


def home(request):
    return render(request, 'ToP/home.html')


def top_rated(request):
    playlist_list = Playlist.objects.order_by("rating")[:40]
    context_dict = {'playlists': playlist_list}
    response = render(request, 'ToP/top_rated.html', context=context_dict)
    return response


def most_viewed(request):
    playlist_list = Playlist.objects.order_by("views")[:40]
    context_dict = {'playlists': playlist_list}
    response = render(request, 'ToP/most_viewed.html', context=context_dict)
    return response


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

        # Flushes the artist art folder to prevent build up of unecessary art
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if os.path.exists(BASE_DIR + '\media\\' + "artist_art\\"):
            shutil.rmtree(BASE_DIR + '\media\\' + "artist_art\\")
            os.makedirs(BASE_DIR + '\media\\' + "artist_art\\")
        elif not os.path.exists(BASE_DIR + '\media\\' + "artist_art\\"):
            os.makedirs(BASE_DIR + '\media\\' + "artist_art\\")

        # Queries the spotify song database and pulls the artist image url from it based on the artist title entered on
        # each song. This is called song.artist_art. If the song art isnt found(this causes the program to pick
        # the last chosen album art) the program checks with the checksum(the url of the previously used album art)
        # and if this is the same as the new url, a default image is used
        checksum = ""
        album_checksum = ""
        check_artist = songs[0].artist

        # Flushes the artist art folder to prevent build up of unecessary art
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        """if os.path.exists(BASE_DIR+'\media\\'+"artist_art\\"):
            shutil.rmtree(BASE_DIR+'\media\\'+"artist_art\\")
            os.makedirs(BASE_DIR+'\media\\'+"artist_art\\")
        elif not os.path.exists(BASE_DIR+'\media\\'+"artist_art\\"):
            os.makedirs(BASE_DIR+'\media\\'+"artist_art\\")
        """
        # Queries the spotify song database and pulls the artist image url from it based on the artist title entered on
        # each song. This is called song.artist_art. If the song art isnt found(this causes the program to pick
        # the last chosen album art) the program checks with the checksum(the url of the previously used album art)
        # and if this is the same as the new url, a default image is used
        checksum = ""
        album_checksum = ""
        for song in songs:
            if song == None:
                check_artist = songs[0].artist
        testfile = urllib.URLopener()

        # Artist Art
        for song in songs:
            results = spotify.search(q='artist:' + song.artist, type='artist')
            items = results['artists']['items']
            if len(items) > 0:
                artist = items[0]
            song.artist_art = artist['images'][0]['url']
            if song.artist_art == checksum and song.artist != check_artist:
                song.artist_art = "https://cdn.pixabay.com/photo/2015/08/10/21/26/vinyl-883199_960_720.png"
                checksum = song.artist_art
            else:
                checksum = song.artist_art
            testfile.retrieve(song.artist_art, BASE_DIR + '\media\\' + "artist_art\\" + str(song.artist) + "_art.jpg")
            song.artist_art = '\media\\' + "artist_art\\" + str(song.artist) + "_art.jpg"
            song.artist_art = artist['images'][0]['url']
            if song.artist_art == checksum and song.artist != check_artist:
                song.artist_art = BASE_DIR + "\media\\vinyl-883199_960_720.png"
                checksum = song.artist_art
            else:
                checksum = song.artist_art
            if not os.path.exists(BASE_DIR + '\media\\' + "artist_art\\" + str(song.artist) + "_art.jpg"):
                testfile.retrieve(song.artist_art,
                                  BASE_DIR + '\media\\' + "artist_art\\" + str(song.artist) + "_art.jpg")
            song.artist_art = '\media\\' + "artist_art\\" + str(song.artist) + "_art.jpg"

            # Album Art
            results = spotify.search(q='album:' + song.title, type='album')
            items = results['albums']['items']
            for item in items:
                if item.get(song.artist) == song.artist:
                    album = item
                else:
                    album = items[0]
                song.album_art = album['images'][0]['url']
                if song.album_art == checksum and song.artist != check_artist:
                    song.album_art = "https://cdn.pixabay.com/photo/2015/08/10/21/26/vinyl-883199_960_720.png"
                    album_checksum = song.album_art
                else:
                    album_checksum = song.album_art
                testfile.retrieve(song.album_art, BASE_DIR + '\media\\' + "artist_art\\" + str(song.title) + "_art.jpg")
                song.album_art = '\media\\' + "artist_art\\" + str(song.title) + "_art.jpg"
                context_dict['album_art'] = song.album_art

        context_dict['artist_art'] = song.artist_art
        album_checksum = song.album_art
    if not os.path.exists(BASE_DIR + '\media\\' + "artist_art\\" + str(song.title) + "_art.jpg"):
        testfile.retrieve(song.album_art, BASE_DIR + '\media\\' + "artist_art\\" + str(song.title) + "_art.jpg")
    song.album_art = '\media\\' + "artist_art\\" + str(song.title) + "_art.jpg"
    context_dict['album_art'] = song.album_art


context_dict['artist_art'] = song.artist_art
except Playlist.DoesNotExist:  # Template will display "no playlist" message for us
context_dict['playlist'] = None
context_dict['songs'] = None

visitor_cookie_handler(request)
context_dict['visits'] = request.session['visits']

response = render(request, 'ToP/playlist.html', context=context_dict)
views = forms.IntegerField(context_dict['visits'], initial=0)

return render(request, 'ToP/playlist.html', context_dict)


@login_required
def add_comment_to_playlist(request, playlist_name_slug):
    playlist = Playlist.objects.get(slug=playlist_name_slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.playlist = playlist
            print playlist
            comment.save()
            return show_playlist(request, playlist_name_slug)
    else:
        form = CommentForm()
    return render(request, 'ToP/add_comment_to_playlist.html', {'form': form})


def view_all_playlists(request):
    # Get a list of all playlists currently stored and order by name ascending
    playlist_list = Playlist.objects.order_by('name')
    # List placed into context dictionary that is passed into template engine
    context_dict = {'playlists': playlist_list}

    return render(request, 'ToP/view_all_playlists.html', context_dict)


# This view is basically like viewing the current user's profile
@login_required
def my_playlists(request):
    # Get a list of all playlists currently stored and order by name ascending
    playlist_list = Playlist.objects.order_by('name')
    # List placed into context dictionary that is passed into template engine
    context_dict = {'playlists': playlist_list}
    return render(request, 'ToP/my_playlist.html', context_dict)


@login_required
def create_playlist(request):
    form = PlaylistForm()

    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)

        # Valid form?
        if form.is_valid():
            form.save(commit=True)
            return home(request)
        else:
            print(form.errors)

    # Render form with error messages, if any
    return render(request, 'ToP/create_playlist.html', {'form': form})


@login_required
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


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # Gets the number of views of the site
    # If the cookie exists, the string value is cast to an integer value and returned
    # Otherwise 1 is used as the default value
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


@csrf_protect
def password_reset(request,
                   is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
        print post_reset_redirect
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == 'POST':
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
        else:
            form = password_reset_form()
        context = {
            'form': form,
            'title': _('Password reset'),
        }
        if extra_context is not None:
            context.update(extra_context)
        return HttpResponseRedirect(request, template_name, context)


def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None,
                        extra_context=None):
    context = {
        'title': _('Password reset successful'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, currrent_app=current_app)


@sensitive_post_parameters()
@never_cache
def passwored_reset_confirm(request,
                            uidb64=None,
                            token=None,
                            template_name='registration/password_reset_confirm.html',
                            set_password_form=SetPasswordForm,
                            token_generator=default_token_generator,
                            post_reset_redirect=None,
                            current_app=None,
                            extra_context=None):
    """View that checks the hash in a password reset link and presents a form for
    entering a new password."""
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModle._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None,
                            extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)


def ResetPasswordRequest(FormView):
    template_name = 'account/test_template.html'
    success_url = '/account/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        associated_users = User.objects.filter(Q(email=data) | Q(username=data))
        if associated_users.exists():
            for user in aassociated_users:
                c = {
                    'email': user.email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'your site',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                subject_template_name = 'registration/password_reset_subject.txt'
                email_template_name = 'registration/password_reset_email.html'
                subject = loader.render_to_string(subject_template_name, c)
                subject = ''.join(subject.splitlines())
                email = loader.render_to_string(email_template_name, c)
                send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            result = self.form_valid(form)
            messages.success(request,
                             'An email has been sent to ' + data + '. Please check your inbox to continue resting your password.')
            return result
        result = self.form_invalid(form)
        messages.error(request, 'No user is associated with this email address.')
        return result


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    warnings.warn("The password_change() view is superseded by the "
                  "class-based PasswordChangeView().",
                  RemovedInDjango21Warning, stacklevel=2)
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         extra_context=None):
    warnings.warn("The password_change_done() view is superseded by the "
                  "class-based PasswordChangeDoneView().",
                  RemovedInDjango21Warning, stacklevel=2)
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
