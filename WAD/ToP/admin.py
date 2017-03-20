from django.contrib import admin
from ToP.models import Playlist, Song, UserProfile
from ToP.models import UserProfile,Comment


class PlaylistAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'genre')

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Rating)