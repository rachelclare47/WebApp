from django import forms


class PlaylistForm(forms.ModelForm):
    """
    class Meta:
        model=Playlist
        fields=('Name','Picture','Songs','Username','Views','Rating')
    """
class SongForm(forms.ModelForm):
    """
    class Meta:
        model=Song
        fields=('Title','Artist','Album','Playlists')
    """
