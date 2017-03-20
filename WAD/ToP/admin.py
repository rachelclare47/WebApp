from django.contrib import admin
from ToP.models import Playlist, Song, UserProfile
from ToP.models import UserProfile,Comment


class PlaylistAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
	'''def save_model(self, request, instance, form, change):
		user = request.user
		instance = form.save(commit=False)
		if not change or not instance.author:
			instance.author = user
		instance.modified_by = user
		instance.save()
		form.save_m2m()
		return instance
	
	def save_model(self, request, obj, form, change):
		if getattr(obj, 'author', None) is None:
			obj.author = request.user
		obj.save()'''


class SongAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'genre')

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile)
admin.site.register(Comment)
