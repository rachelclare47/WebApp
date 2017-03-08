from django.contrib import admin
from ToP.models import Playlist, Song
from ToP.models import UserProfile


class PlaylistAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}


class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'genre')

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile)