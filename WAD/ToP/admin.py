from django.contrib import admin
from ToP.models import Playlist, Song, UserProfile, Comment, Rating


class PlaylistAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
	

class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'genre')
	

# Registers classes to the admin interface
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Rating)
