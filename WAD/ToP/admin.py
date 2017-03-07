from django.contrib import admin
from ToP.models import Playlist, Song

class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'genre')

admin.site.register(Playlist)
admin.site.register(Song, SongAdmin)