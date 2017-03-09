from django import forms
from django.contrib.auth.models import User
from ToP.models import Playlist, Song, UserProfile


class PlaylistForm(forms.ModelForm):

    class Meta:
        model=Playlist
        fields=('name','picture','author','views','rating','slug')


class SongForm(forms.ModelForm):
    """
    class Meta:
        model=Song
        fields=('Title','Artist','Album','Playlists')
    """


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
