from django import forms
from django.contrib.auth.models import User
from ToP.models import Playlist, Song, UserProfile


class PlaylistForm(forms.ModelForm):
<<<<<<< HEAD
    name = forms.CharField(max_length=128, help_text="Please enter the playlist name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    picture = forms.ImageField()
    ##############################################################
    # FIGURE OUT HOW TO PUT USER URL IN INITIAL HIDDEN FIELD
    author = forms.URLField(widget=forms.HiddenInput(), initial="https://ToP/admin/user")
    ##############################################################
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Playlist
        fields = ('name', 'picture', 'author',)
=======

    class Meta:
        model=Playlist
        fields=('name','picture','author','views','rating','slug')
>>>>>>> aff045ad7040d4abad5ec5be52ecdf2ba99abe87


class SongForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the song.")
    artist = forms.CharField(max_length=128, help_text="Please enter the artist of the song.")
    genre = forms.CharField(max_length=128, help_text="Please enter the genre of music.")
    
    class Meta:
        model = Song
        # Hiding the foreign key
        # Can either exclude the playlist field from the form or specify fields to include
        exclude = ('playlists',)
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
